import json


def get_book_subjects():
    with open('app/files/books.json', 'r') as f:
        subjects = json.load(f)
        f.close()
    return list(subjects.keys())


def get_book_items(key):
    with open('app/files/books.json', 'r') as f:
        subjects = json.load(f)
        f.close()
    return subjects[key]


def get_tickets_subjects():
    with open('app/files/tickets.json', 'r') as f:
        subjects = json.load(f)
        f.close()
    return list(subjects.keys())


def get_tickets_items(key):
    with open('app/files/tickets.json', 'r') as f:
        subjects = json.load(f)
        f.close()
    return subjects[key]


def add_book(subject, name):
    with open('app/files/books.json', 'r') as f:
        files = json.load(f)
        f.close()
    files[subject].append(name)
    with open('app/files/books.json', 'w') as f:
        json.dump(files, f)
        f.close()


def add_tickets(subject, name):
    with open('app/files/tickets.json', 'r') as f:
        files = json.load(f)
        f.close()
    files[subject].append(name)
    with open('app/files/tickets.json', 'w') as f:
        json.dump(files, f)
        f.close()


def add_subject_book(subject):
    with open('app/files/books.json', 'r') as f:
        files = json.load(f)
        f.close()
    files[subject] = []
    with open('app/files/books.json', 'w') as f:
        json.dump(files, f)
        f.close()


def add_subject_tickets(subject):
    with open('app/files/tickets.json', 'r') as f:
        files = json.load(f)
        f.close()
    files[subject] = []
    with open('app/files/tickets.json', 'w') as f:
        json.dump(files, f)
        f.close()
