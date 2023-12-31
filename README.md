# АУТЕНТИФИКАЦИЯ И ИДЕНТИФИКАЦИЯ ПОЛЬЗОВАТЕЛЕЙ

| Вариант | Метод установления подлинности         | 
|---------|----------------------------------------|
| 5       | Простой пароль + дополнительные        | 
|         |  требования к виду пароля: минимальное | 
|         |  количество символов, применение       |
|         |  символов различных групп (цифровых,   |
|         |  верхнего и нижнего регистров)         |  

|                   Пояснение                      |
|--------------------------------------------------|
| При введении нового или замене старого пароля    |
| происходит проверка, цель которой – определить   |
| содержит ли пароль заданное кол-во               |
| определенных групп символов. Если не             |
| содержит, то пароль не принимается.              |

Выполнили: 
1. Зайцев И.В.
2. Дощинский М.С.

Структура командного процессора (блок «защита на уровне пользователя»)

Субъекты: Суперпользователь/администратор, другие пользователи - админка

Объекты: база учетных записей пользователей -  SQlite

Минимальный набор команд
1. изменение своего пароля - доступно
2. добавление нового пользователя - доступно, как на странице регистрации, так и со стороны администратора
3. удаление пользователя - доступно со стороны администратора
4. изменение учетной записи пользователя (изменение логина, дополнительных полей
учетной записи (если они есть)) - доступно со стороны администратора
5. просмотр информации о текущем пользователе - доступно со стороны администратора
6. просмотр разрешенной информации о существующих в системе пользователях доступно со стороны администратора
7. несколько нейтральных команд (дата, время, список доступных команд системы и
т.п.). - в качестве аналога данному консольному функционалу реализована система создания тикетов

Минимальная функциональность
1. пароль не должен быть виден на экране +
2. в системе всегда присутствует хотя бы один суперпользователь +
3. обыкновенный пользователь ограничен в действиях + 
4. создаёт новых пользователей (удаляет существующих) только суперпользователь - ввиду применения веб создание доступно на странице входа, удаление же только админом
5. суперпользователь может изменять пароли всех пользователей +
6. при изменении/добавлении пароля запрашивается его подтверждение +
7. имена пользователей в системе попарно различны (не повторяются) +
8. возможность зайти под другим пользователем, не закрывая приложение +
9. работать в системе может только пользователь, успешно прошедший процедуру
аутентификации +
