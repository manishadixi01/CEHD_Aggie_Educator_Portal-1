import datetime
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from .models import StudentPlacements
from core.models import Person
from utils.utility import get_current_semester, get_current_year


def query_student_list_details(email):
    """
    Helper function to get the student details from list of emails
    """
    if not email:
        pass
    person_tmp = Person.objects.all().filter(primary_email__in=email)
    person_tmp = json.loads(serializers.serialize('json', person_tmp))
    person_details_list = list()
    person_details = dict()
    for pd in person_tmp:
        tmp = dict()
        tmp["first_name"] = pd["fields"]["first_name"]
        tmp["middle_name"] = pd["fields"]["middle_name"]
        tmp["last_name"] = pd["fields"]["last_name"]
        tmp["primary_email"] = pd["fields"]["primary_email"]
        if pd["fields"].get("middle_name", "").strip() == "":
            tmp["full_name"] = pd["fields"]["first_name"] + " " + pd["fields"]["last_name"]
        else:
            tmp["full_name"] = pd["fields"]["first_name"] + " " + pd["fields"]["middle_name"].strip() \
                               + " " + pd["fields"]["last_name"]
        person_details_list.append(pd)
        person_details[pd["fields"]["primary_email"]] = tmp["full_name"]
    return person_details, person_details_list


def query_student_details(email, uin=None):
    """
    Helper function to get the student details from email or UIN
    """
    if not email and not uin:
        pass
    person_details = None
    if email:
        person_details = Person.objects.all().filter(primary_email=email)
    elif uin:
        person_details = Person.objects.all().filter(uin=uin)
    if person_details:
        person_details = json.loads(serializers.serialize('json', person_details))
        person_details = person_details[0]["fields"]
        tmp = dict()
        tmp["first_name"] = person_details["first_name"]
        tmp["middle_name"] = person_details["middle_name"]
        tmp["last_name"] = person_details["last_name"]
        tmp["primary_email"] = person_details["primary_email"]
        tmp["secondary_email"] = person_details["secondary_email"]
        if person_details.get("middle_name", "").strip() == "":
            tmp["full_name"] = person_details["first_name"] + " " + person_details["last_name"]
        else:
            tmp["full_name"] = person_details["first_name"] + " " + person_details[
                "middle_name"].strip() + " " + person_details["last_name"]
        person_details = tmp
    return person_details


def query_student_placements_email(email, semester):
    """
    Helper function to query the student placements table for information based on student email and/or semester
    """
    with open("config.json") as json_config_file:
        config = json.load(json_config_file)
    if not semester:
        today_date = datetime.date.today()
        for k, v in config["semester"].items():
            sem_start = today_date.replace(month=v["start_month"], day=v["start_day"])
            sem_end = today_date.replace(month=v["end_month"], day=v["end_day"])
            if sem_start <= today_date <= sem_end:
                semester = k
                break
    sp_items = StudentPlacements.objects.all().filter(student_email=email, semester=semester).distinct("student_email",
                                                                                                       "semester")
    sp_item_serializer = json.loads(serializers.serialize('json', sp_items))
    return sp_item_serializer


def query_student_placements_uin(uin, semester):
    """
    Helper function to query the student placements table for information based on student UIN and/or semester
    """
    with open("config.json") as json_config_file:
        config = json.load(json_config_file)
    if not semester:
        today_date = datetime.date.today()
        for k, v in config["semester"].items():
            sem_start = today_date.replace(month=v["start_month"], day=v["start_day"])
            sem_end = today_date.replace(month=v["end_month"], day=v["end_day"])
            if sem_start <= today_date <= sem_end:
                semester = k
                break
    sp_items = StudentPlacements.objects.all().filter(uin=uin, semester=semester).distinct("uin", "semester")
    sp_item_serializer = json.loads(serializers.serialize('json', sp_items))
    return sp_item_serializer


def query_supervisor_email(email, semester):
    """
    Helper function to query the student placements table for information based on supervisor email and/or semester
    """
    kwargs = dict()
    with open("config.json") as json_config_file:
        config = json.load(json_config_file)
    kwargs["university_supervisor_email"] = email
    if semester:
        kwargs["semester"] = config["reverse_semester"][semester]
    sp_items = StudentPlacements.objects.all().filter(**kwargs) \
        .distinct("university_supervisor_email", "cooperating_teacher_email")
    sp_item_serializer = json.loads(serializers.serialize('json', sp_items))
    return sp_item_serializer


class StudentPlacementsGet(APIView):
    """
    Query the student placements table for information based on student email and/or semester
    """

    def get(self, request, email, semester=None):
        """
        GET function to query the student placements table for information based on student email and/or semester
        """
        sp_item_serializer = query_student_placements_email(email, semester)
        if len(sp_item_serializer) > 0:
            sp_item_serializer = sp_item_serializer[0]
        else:
            sp_item_serializer = None
        return Response({"status": "success", "data": sp_item_serializer}, status=status.HTTP_200_OK)


class SupervisorGet(APIView):
    """
    Query the student placements table for information based on supervisor email and/or semester
    """

    def get(self, request, email, semester=None):
        """
        GET function to query the student placements table for information based on supervisor email and/or semester
        """
        sp_item_serializer = query_supervisor_email(email, semester)
        if len(sp_item_serializer) < 0:
            sp_item_serializer = None
        return Response({"status": "success", "data": sp_item_serializer}, status=status.HTTP_200_OK)


def get_student_super_coop(supervisor_email, cooperating_teacher_email):
    """
    Helper function to query the student placements table for information based on supervisor email and cooperating teacher email
    """
    student_list = StudentPlacements.objects.all().filter(university_supervisor_email=supervisor_email,
                                                          cooperating_teacher_email=cooperating_teacher_email) \
        .distinct("student_email")
    student_serializer = json.loads(serializers.serialize('json', student_list))
    student_list_serializer = list()
    for data in student_serializer:
        student_list_serializer.append(data["fields"]["student_email"])
    return student_list_serializer


def get_coop_student_current(cooperating_teacher_email):
    """
    Helper function to query the student placements table for students information based on cooperating teacher email and
    semester
    """
    semester, semester_ui = get_current_semester()
    semester_year = get_current_year()
    student_list = StudentPlacements.objects.all().filter(cooperating_teacher_email=cooperating_teacher_email,
                                                          semester_year=semester_year, semester=semester).distinct(
        "student_email")
    student_serializer = json.loads(serializers.serialize('json', student_list))
    student_current_serializer = dict()
    student_current_serializer["cooperating_teacher_email"] = cooperating_teacher_email
    student_current_serializer["semester"] = semester_ui
    student_current_serializer["semester_year"] = semester_year
    student_current_serializer["students"] = list()
    for data in student_serializer:
        if student_current_serializer.get("university_supervisor_email", None) is None:
            student_current_serializer["university_supervisor_email"] = data["fields"]["university_supervisor_email"]
        if student_current_serializer.get("university_supervisor", None) is None:
            student_current_serializer["university_supervisor"] = data["fields"]["university_supervisor"]
        if student_current_serializer.get("cooperating_teacher", None) is None:
            student_current_serializer["cooperating_teacher"] = data["fields"]["cooperating_teacher"]
        student_current_serializer["students"].append(query_student_details(data["fields"]["student_email"]))
    return student_current_serializer, semester


def get_super_coop_details(supervisor_email, coop_email):
    """
    helper function to retrieve the supervisor and cooperating teacher details
    """
    detail = StudentPlacements.objects.all().filter(university_supervisor_email=supervisor_email,
                                                    cooperating_teacher_email=coop_email)\
        .distinct("university_supervisor_email", "cooperating_teacher_email")
    detail_serializer = json.loads(serializers.serialize('json', detail))
    return detail_serializer


def query_coop_email(coop_email, semester):
    """
    helper function to get the list of students based on cooperating teacher email
    """
    kwargs = dict()
    with open("config.json") as json_config_file:
        config = json.load(json_config_file)
    kwargs["cooperating_teacher_email"] = coop_email
    if semester:
        kwargs["semester"] = config["reverse_semester"][semester]
    students_list = StudentPlacements.objects.all().filter(**kwargs).distinct("student_email")
    students_list_serializer = json.loads(serializers.serialize('json', students_list))
    students = set()
    for st in students_list_serializer:
        students.add(st["fields"]["student_email"])
    return students_list_serializer, list(students)
