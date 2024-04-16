from requests import Response
import json, random, string, re, hashlib, uuid
from datetime import datetime, timedelta, timezone

class Util():

    def __init__(self):
        self.auth_first_token = None

    def init(self, session, config, logger):
        sessionToken = None

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def generate_data(self):
        # берем дату сегодня
        nowDate = datetime.now(timezone.utc)
        delta = timedelta(days=15)
        todayDate = nowDate.strftime("%Y-%m-%dT%H:%M:%S")
        # создаем дату на 5 дней вперед
        newFutureDate = nowDate + delta
        futureDate = newFutureDate.strftime("%Y-%m-%dT%H:%M:%S")
        # создаем дату на 5 дней назад
        newLastDate = nowDate - delta
        lastDate = newLastDate.strftime("%Y-%m-%dT%H:%M:%S")

        nowDay = nowDate.strftime("%Y-%m-%d")
        nowTime = nowDate.strftime("%H:%M:%S")

        return [futureDate, lastDate, todayDate, nowDay, nowTime]

    # генерация времени без часового пояса
    def start_and_current_date(self):
        # Получаем текущее время в UTC
        current_time = datetime.now(timezone.utc)

        # Получаем начало суток в UTC 0
        start_of_day_utc_0 = datetime(current_time.year, current_time.month, current_time.day, tzinfo=timezone.utc)

        # Форматируем даты
        startDay = start_of_day_utc_0.strftime("%Y-%m-%dT%H:%M:%S")
        currentTime = current_time.strftime("%Y-%m-%dT%H:%M:%S")

        return startDay, currentTime

    def generate_random_string(self):
        length = 10
        letters = string.ascii_lowercase
        randomString = ''.join(random.choice(letters) for i in range(length))
        return randomString

    def generate_string_for_push(self):
        length = 163
        letters = string.ascii_lowercase
        randomString = ''.join(random.choice(letters) for i in range(length))
        return randomString

    @staticmethod
    def elements_in_dict(response: Response, name):
        # Ищу по паттерну количество элементов
        dictionary = response.text
        pattern = fr"{name}"
        all_mathces = len(re.findall(pattern,  dictionary))

        return all_mathces
    @staticmethod
    def random_entity_id(response: Response, objectName, keyName):
        json_dict = response.json()
        entityID = random.choice(json_dict[f"{objectName}"])[f"{keyName}"]

        return entityID

    @staticmethod
    def find_entity_id_with_special_key_value(response: Response, objectName: str, keyName: str, checkName: str):
        json_dict = response.json()
        filtered_messages = []
        entityID = None

        messages = json_dict[objectName]
        for i in messages:
            if checkName in i and i[checkName] == 1:
                filtered_messages.append(i[keyName])
                entityID = random.choice(filtered_messages)
                assert entityID != None, f"Couldnt get an entity ID, check this test!"
        return entityID

    @staticmethod
    def find_entity_id_with_exist_key_in_dict(response: Response, objectName: str, keyName: str, endKey: str):
        # получаем задачу
        json_dict = response.json()
        tasks = json_dict[objectName]
        entityID = int
        taskID = int
        task_checklist_mapping = []
        # Проходимся по каждой задаче
        for task in tasks:
            # Проверяем наличие блока checkLists
            if keyName in task:
                # Проходимся по каждому чеклисту в задаче
                for checklist in task["checkLists"]:
                    # Добавляем соответствие taskID и checklistExternalID в список
                    taskID = task["taskID"]
                    entityID = checklist["checklistExternalID"]
                    task_checklist_mapping.append((task["taskID"], checklist["checklistExternalID"]))

        return entityID, taskID

    @staticmethod
    def find_entity_id_with_notExist_key(response: Response, objectName: str, keyName: str, checkName: str):
        json_dict = response.json()
        filtered_messages = []
        entityID = None

        messages = json_dict[objectName]
        for i in messages:
            if checkName not in i:
                filtered_messages.append(i[keyName])
                entityID = random.choice(filtered_messages)

        return entityID

    @staticmethod
    def dict_of_entity_ids(response: Response, objectName, keyName):
        json_dict = response.json()
        entityIDs = [e[f'{keyName}'] for e in json_dict[f"{objectName}"]]

        return entityIDs

    @staticmethod
    def hash_password(session: str, password: str):
        md5Password = hashlib.md5(password.encode()).hexdigest()
        sessionPass = f"{session}{md5Password}"
        passwordHash = hashlib.md5(sessionPass.encode()).hexdigest()

        return  passwordHash

    @staticmethod
    def random_app_type():
        types = [1,2,3,4]
        randomType = random.choice(types)

        return randomType

    @staticmethod
    def count_entity_ids(response: Response, objectName, keyName):
        json_dict = response.json()
        entityID = len([e[f'{keyName}'] for e in json_dict[f"{objectName}"]])

        return entityID

    @staticmethod
    def generate_uuid():
        myuuid = uuid.uuid4()
        myuuidStr = str(myuuid)

        return myuuidStr

    @staticmethod
    def choose_ids(response: Response, objectName, keyName):
        json_dict = response.json()
        ids = []
        badValue = -1
        entityIDs = sorted([e[f'{keyName}'] for e in json_dict[f"{objectName}"]])
        for i in entityIDs:
            if i != badValue:
                ids.append(i)

        return ids
    @staticmethod
    def get_urns(response: Response, objectName, keyName):
        json_dict = response.json()
        objectName = json_dict[f"{objectName}"]
        fileUrns = []
        for item in json_dict:
            fileUrns= [e["fileUrn"] for e in objectName]

        return fileUrns

    @staticmethod
    def get_locations_form_object(response: Response, keyName, entityID):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is '{response.text}'"
        longitude = float
        latitude = float
        objectResp = response_as_dict["objects"]
        for objectName in objectResp:
            if keyName in objectName and objectName[keyName] == entityID:
                longitude = objectName["longitude"]
                latitude = objectName["latitude"]

        return [longitude, latitude]


    @staticmethod
    def create_form_by_template(response: Response, entityUUID: str, externalIDs=None, externalID=None, taskID=None, messageID=None, checkinID=None, objectID=None, isDraft=None, addInfo=None, location=None):
        json_dict = response.json()
        templates = json_dict["templates"]
        entityID = externalID
        entityIDs = externalIDs

        if externalID is None and externalIDs is None:
            entityID = str
            entityIDs = []
            for template in templates:
                templateType = template["formTemplateType"]
                amount = len([e["formTemplateItemID"] for e in template["items"]])

                if amount <= 21 and templateType == 0:
                    entityIDs.append(template["externalID"])

        new_json_list = []

        for entityID in entityIDs:
            newTemplate = next((template for template in templates if "externalID" in template and template["externalID"] == entityID), None)

            if newTemplate is None:
                continue  # Если не удалось найти шаблон по externalID, пропустить текущую итерацию

            new_json = {"formUUID": entityUUID, "formTemplateExternalID": entityID, "items": [], "location": location}

            if taskID is not None:
                new_json["taskID"] = taskID
            if messageID is not None:
                new_json["messageID"] = messageID
            if checkinID is not None:
                new_json["checkinID"] = checkinID
            if objectID is not None:
                new_json["objectID"] = objectID
            if isDraft is not None:
                new_json["isDraft"] = isDraft
            if addInfo is not None:
                new_json["addInfo"] = addInfo

            for item in newTemplate["items"]:
                value, values, files = None, [], None
                order = 0
                if 0 <= item["type"] <= 1:
                    value = Util.generate_random_string(Util)  # Генерация рандомной строки
                elif item["type"] == 2:
                    value = Util.generate_data(Util)[3]
                elif item["type"] == 3:
                    value = Util.generate_data(Util)[4]
                elif 4 <= item["type"] <= 5:
                    value = 123
                elif item["type"] == 6:
                    value = random.choice(["true", "false"])
                elif item["type"] == 7:
                    if item.get("subType") == 2:
                        values = random.sample(item["optionList"], 3)
                    else:
                        value = random.choice(item["optionList"])
                elif item["type"] == 8:
                    value = Util.generate_uuid()
                    files = [{"fileName": "photo_pytest.jpg", "contentType": "image/jpeg", "contentLength": 123, "order": order}]
                elif item["type"] == 9:
                    value = Util.generate_uuid()
                    files = [{"fileName": "pytest.txt", "contentType": "text/plain", "contentLength": 123, "order": order}]

                new_item = {
                    "formTemplateItemID": item["formTemplateItemID"],
                    "value": value,
                    "values": values,
                    "metadata": files
                }
                new_json["items"].append(new_item)

            new_json_list.append(new_json)

        return new_json_list

    @staticmethod
    def create_checkList_by_template(response: Response, entityUUID: str, taskID=None, isDraft=None, addInfo=None, location=None):
        json_dict = response.json()
        items = json_dict["items"]
        checklistExternalID = json_dict["checklistExternalID"]

        new_json = {"formUUID": entityUUID, "items": [], "location": location, "checklistExternalID": checklistExternalID}

        if taskID is not None:
            new_json["taskID"] = taskID
        if isDraft is not None:
            new_json["isDraft"] = isDraft
        if addInfo is not None:
            new_json["addInfo"] = addInfo

        for item in items:
                value, values, files = None, [], None
                order = 0
                if 0 <= item["type"] <= 1:
                    value = Util.generate_random_string(Util)  # Генерация рандомной строки
                elif item["type"] == 2:
                    value = Util.generate_data(Util)[3]
                elif item["type"] == 3:
                    value = Util.generate_data(Util)[4]
                elif 4 <= item["type"] <= 5:
                    value = 123
                elif item["type"] == 6:
                    value = random.choice(["true", "false"])
                elif item["type"] == 7:
                    if item.get("subType") == 2:
                        values = random.sample(item["optionList"], 3)
                    else:
                        value = random.choice(item["optionList"])
                elif item["type"] == 8:
                    value = Util.generate_uuid()
                    files = [{"fileName": "photo_pytest.jpg", "contentType": "image/jpeg", "contentLength": 123, "order": order}]
                elif item["type"] == 9:
                    value = Util.generate_uuid()
                    files = [{"fileName": "pytest.txt", "contentType": "text/plain", "contentLength": 123, "order": order}]

                new_item = {
                        "formTemplateItemID": item["formTemplateItemID"],
                        "value": value,
                        "values": values,
                        "metadata": files
                    }

                new_json["items"].append(new_item)

        return new_json


    @staticmethod
    def change_form_by_template(data):

        # Преобразование значений параметра "value" в соответствующий тип
        for item in data["items"]:
            value = str(item["value"])
            if value.isdigit():
                item["value"] = int(value)
            elif value.replace('.', '', 1).isdigit():
                item["value"] = float(value)
            elif value.lower() == 'true' or value.lower() == 'false':
                item["value"] = value.lower() == 'true'
            elif value.lower() == 'null':
                item["value"] = None

        return data
    @staticmethod
    def find_template_with_photo_item(response: Response):
        json_dict = response.json()
        templates = json_dict["templates"]
        entityIDs = set()  # используем множество для хранения уникальных externalID

        for template in templates:
            templateType = template["formTemplateType"]
            amount = len([e["formTemplateItemID"] for e in template["items"]])
            types = [e["type"] for e in template["items"]]

            if amount <= 30 and templateType == 0:
                for itemType in types:
                    if itemType == 8:
                        externalID = template["externalID"]
                        if externalID not in entityIDs:  # проверяем, есть ли уже такой externalID
                            entityIDs.add(externalID)
                            break  # добавляем только один раз, затем выходим из внутреннего цикла

        return list(entityIDs)  # преобразуем множество обратно в список для возвращения результата

    @staticmethod
    def find_task_id_with_status_formTemplates(response: Response, taskStatus: int):
        # получаем задачу и выбираем ту что в не конечном статусе и с формами
        json_dict = response.json()
        tasks = json_dict["tasks"]
        entityIDs = []

        # Выбираем все задачи, у которых есть формы с нужным статусом
        for task in tasks:
            if "statusFormTemplates" in task and task["status"] == 0:
                if any(i.get("taskStatus") == taskStatus for i in task["statusFormTemplates"]):
                    entityIDs.append(task["taskID"])

        if not entityIDs:
            return None, None

        # Выбираем случайную задачу из подходящих
        entityID = random.choice(entityIDs)

        # Находим формы с нужным статусом для выбранной задачи
        formTemplateExternalID = []
        for task in tasks:
            if task["taskID"] == entityID:
                for i in task["statusFormTemplates"]:
                    if "taskStatus" in i and i["taskStatus"] == taskStatus:
                        formTemplateExternalID.append(i["formTemplateExternalID"])
                break

        # возвращаем ИД задачи и список экстерналов
        return entityID, formTemplateExternalID

    @staticmethod
    def find_task_id_with_required_comment(response: Response, commentPolicy: int):

        try:
            # получаем задачу и выбираем ту что новая и с формами
            json_dict = response.json()
            tasks = json_dict["tasks"]
            entityIDs = []
            for task in tasks:
                if "commentPolicy" in task and task["commentPolicy"] == commentPolicy:
                    entityIDs.append(task["taskID"])
            entityID = random.choice(entityIDs)

            return entityID
        except:
            print("Нет таких задач!")


    @staticmethod
    def find_fresh_task(response: Response):

        # получаем задачу и выбираем ту что новая и с формами
        json_dict = response.json()
        tasks = json_dict["tasks"]
        entityIDs = []
        nowDate = datetime.now(timezone.utc)
        delta = timedelta(days=15)

        # создаем дату на n-дней назад
        newLastDate = nowDate - delta
        lastDate = newLastDate.strftime("%Y-%m-%dT%H:%M:%S")
        taskStatus = int

        #Выбираем задачу посвежее, если дата не старше чем 15 дней назад
        for task in tasks:
            if task["creationDate"] >= lastDate:
                    entityIDs.append(task["taskID"])
        entityID = random.choice(entityIDs)

        for task in tasks:
            if task["taskID"] == entityID:
                taskStatus = task["status"]

        # возвращаем ИД задачи и ее статус
        return [entityID, taskStatus]

    @staticmethod
    def find_external_ids_with_content_fields(json_data):
        form_item_dict_with_image = {}
        form_item_dict_with_files = {}

        for item in json_data["filesData"]:
            form_template_item_id = item["formTemplateItemID"]
            files = item.get("files")

            if files is not None and isinstance(files, list) and len(files) > 0:
                for i in files:
                    content_type = i.get("contentType")
                    fileUrn = i.get("fileUrn")
                    if content_type == "image/jpeg":
                        form_item_dict_with_image.update({form_template_item_id : fileUrn})

                    elif content_type == "text/plain":
                        form_item_dict_with_files.update({form_template_item_id : fileUrn})

        return form_item_dict_with_image, form_item_dict_with_files

    @staticmethod
    def fill_attach(formTemplateItemIds):

        # Списки итемов на которые надо отправить контент
        formTemplateImages = formTemplateItemIds[0]
        formTemplateFiles = formTemplateItemIds[1]
        photo = open('testFiles/photo_pytest.jpg', 'rb')
        file = open('testFiles/pytest.txt', 'rb')

        # Если у нас есть урны и итемы в ответе, то можем залить контент файлов в свои урны

        photo_in_param = {'file': ('photo_pytest.jpg', photo, 'image/jpeg', {"type": "formData"})}
        file_in_param = {'file': ('pytest.txt', file, 'text/plain', {"type": "formData"})}
        output_dict = {}

        if formTemplateImages is not None and formTemplateFiles is not None:
            for key, value in formTemplateImages.items():
                formTemplateItemID = key
                urn = value
                files = photo_in_param
                output_dict[key] = {'formTemplateItemID': formTemplateItemID, 'urn': urn, 'files': files}

            for key, value in formTemplateFiles.items():
                formTemplateItemID = key
                urn = value
                files = file_in_param
                output_dict[key] = {'formTemplateItemID': formTemplateItemID, 'urn': urn, 'files': files}

        return output_dict, photo, file







