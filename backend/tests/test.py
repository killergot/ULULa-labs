import requests
import time

BASE_URL = "https://rasp.spbstu.ru"

def get_all_groups():
    """Получает все группы напрямую через API."""
    r = requests.get(f"{BASE_URL}/api/v1/groups")
    if r.status_code == 200:
        return r.json()
    return []

def get_schedule_by_group(group_id):
    """Получает расписание по ID группы."""
    r = requests.get(f"{BASE_URL}/api/v1/schedule/group/{group_id}")
    if r.status_code == 200:
        return r.json()
    return None

def extract_subjects(schedule_json):
    """Извлекает названия предметов из JSON расписания."""
    subjects = set()
    for day in schedule_json.get("days", []):
        for lesson in day.get("lessons", []):
            subj = lesson.get("subject")
            if subj:
                subjects.add(subj.strip())
    return subjects

def main():
    all_subjects = set()
    groups = get_all_groups()
    print(f"Найдено групп: {len(groups)}")

    for idx, group in enumerate(groups):
        group_id = group.get("id")
        group_title = group.get("title", "")
        print(f"[{idx+1}/{len(groups)}] Группа: {group_title}")

        schedule = get_schedule_by_group(group_id)
        if schedule:
            subjects = extract_subjects(schedule)
            all_subjects.update(subjects)
        time.sleep(0.1)

    print("\n✅ Уникальных предметов найдено:", len(all_subjects))
    for subj in sorted(all_subjects):
        print("-", subj)

if __name__ == "__main__":
    main()