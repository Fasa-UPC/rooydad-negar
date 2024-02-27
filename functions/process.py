import os
import csv


def save_to_csv(data, filename):
    directory = 'media/state'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        date_head = ['پرداختی', 'رشته', 'شماره تماس', 'سال ورود', 'شماره دانشجویی', 'نام خانوادگی', 'نام']
        writer.writerow(date_head)
        for item in data:
            data_row = [item.total, item.user.field_of_study, item.user.phone_number, item.user.entering_year,
                        item.user.student_code, item.user.last_name, item.user.first_name]
            writer.writerow(data_row)

    return file_path
