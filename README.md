# goit-ds-hw-01

### Завдання 1

Скористайтеся будь-яким зручним інструментом pipenv або poetry, на ваш вибір, для створення віртуального середовища для вашої програми

1. Встановлюємо poetry 
   
   curl -sSL https://install.python-poetry.org | python3 -
2. Ініціалізуємо проект goit-pycore-hw-08 
   
   poetry init
3. Додаємо залежності (також для розробника)
   
   poetry add colorama 
   
   poetry add pylint --dev
4. Можна активувати середовище 
   
   poetry shell

### Завдання 2

Створіть Dockerfile, в якому встановіть домашню роботу "Персональний помічник" та запустіть його як окремий застосунок в окремому контейнері

1. Створюємо докерфайл
2. Створюємо образ 
   
   docker build -t goit-pycore-hw-08 .
![Знімок екрана 2025-07-10 о 14.21.05.png](../../../../../var/folders/3c/_d492k1s3wd9cmrkd2tzf38h0000gn/T/TemporaryItems/NSIRD_screencaptureui_7oZKpM/%D0%97%D0%BD%D1%96%D0%BC%D0%BE%D0%BA%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-07-10%20%D0%BE%2014.21.05.png)
3. Запускаємо контейнер у терміналі 
   
   docker run --rm -it goit-pycore-hw-08
![Знімок екрана 2025-07-10 о 14.20.16.png](../../../../../var/folders/3c/_d492k1s3wd9cmrkd2tzf38h0000gn/T/TemporaryItems/NSIRD_screencaptureui_vQwJwq/%D0%97%D0%BD%D1%96%D0%BC%D0%BE%D0%BA%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-07-10%20%D0%BE%2014.20.16.png)