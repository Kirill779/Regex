import re
import csv


def update_phone(ed_file):
    #Считываем данные с файла
    with open(ed_file, encoding="utf8") as f:
        text = f.read()
    #Изменяем вид телефонов
    pattern = r'(\+7|8)?\s*\(?(\d\d\d)\)?[\s*-]?(\d\d\d)[\s*-]?(\d\d)[\s*-]?(\d\d)(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
    update_phone = re.sub(pattern, r'+7(\2)\3-\4-\5\6\7\8', text)
    #Записываем обратно в файл
    with open(ed_file, 'w+', encoding="utf8") as f:
        text = f.write(update_phone)
    return

def  form_list(contacts_list):
    #Правим список, создаём копию списка
    contacts_list2 = []
    for i in contacts_list:
        ux = []   #Переменная список для фамилии, имени, отчества
        fn = i[3:] #Переменная для остальных данных списка.
        if i[1] == '':  # Если имя и отчество не разделены с фамилией
            if i[2]== '': # если отчество не разделено с фамилией
                ux = i[0].split()
                if len(ux) < 3: #если его нету
                    ux += ' '
            else:
                ux = (i[0]+' '+i[1]).split()  #объединяем фамилию и имя при отсутствии отчества
        # Фамилия или имя не могут отсутствовать
        else:
            ux = (i[0]+' '+i[1]+' '+i[2]).split()
        fx = ux +  fn  #соединяем ФИО в новый список
        contacts_list2.append(fx)
    return contacts_list2

def fixing_list(contacts_list):
    #Сначала дублируем наш список
    contacts_list2 = contacts_list
    # Ищем строки в которых один и тот же человек по фамилили и имени
    for i in contacts_list:
        x = 0  # переменная, для определения встречается ли связка фамилия и имя больше 1 раза
        vsc = 0 # переменная для запоминания номера удаляемой строки
        for j  in range(len(contacts_list2)):
            # Сравниваем фамилию и имя
            if (contacts_list2[j][0] + contacts_list2[j][1]) == (i[0] + i[1]):
                x += 1
                if x > 1: # Если встречается больше одного раза то, проверяем строки и объединяем их
                    y = 0
                    for u in contacts_list2[j]:
                        if u != i[y]:
                            if len(contacts_list2[j][y]) > 1:
                                i[y] = contacts_list2[j][y]
                                vsc = j # запоминаем номер лишней строки для удаления
                        y += 1
        if x > 1:
            del contacts_list2[vsc]

    return contacts_list2




if __name__ == '__main__':
    #Приводим телефоны в соответсвующий формат
    update_phone("ok_raw.csv")

    with open("ok_raw.csv", encoding='utf-8',newline='' ) as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

   # for i in contacts_list:
     #print(i[0], i[1], i[2],i[3],i[4])
    #Исправляем сочетание ФИО
    contacts_list2 = form_list(contacts_list)
    #for i in contacts_list2:
     #print([0]),i[1],i[2])#,i[3],i[4])
    # Объединяем лишние строки в одну
    contacts_list = fixing_list(contacts_list2)
    #for i in contacts_list2:
    #   print(i)
    with open("phonebook.csv","w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)



