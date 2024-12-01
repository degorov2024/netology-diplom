# Дипломная работа профессии «Python-разработчик с нуля»
по программе онлайн-курса "Python-разработчик с нуля" ООО "Нетология"

## Разработка Backend приложения для социальной сети для обмена фотографиями

## Цель дипломной работы

Разработка API для загрузки публикаций и их фото с возможностью комментировать и ставить лайки.


## Инструкция к работе над проектом

### Описание задания

Необходимо разработать backend приложения для социальной сети для обмена фотографиями. Прототип фронтенда приложения на скрине:

![](https://github.com/netology-code/spd-diplom/blob/main/Design.png)

В этом проекте вы будете работать над API для загрузки публикаций и их фото с возможностью комментировать и ставить лайки.


### Реализация

Посты должны состоять из текста и фотографии, также должно сохраняться время создания поста.

Публикации могут создаваться только авторизованными пользователями, редактировать же публикацию может только её автор.

Комментарии могут быть написаны к определённой публикации, оставлять их могут только авторизованные пользователи. 
Сам комментарий состоит из текста и даты его публикации.

Помимо комментариев, пользователи также могут оставлять реакцию на публикацию в виде лайка.

При получении деталей публикации помимо полей самой публикации должен отображаться список комментариев и количество 
лайков к публикации, например:

```json
{
  "id": 1,
  "text": "Новый прекрасный день",
  "image": "/posts/image1.jpg",
  "created_at": "2024-02-23T02:24:29.338414",
  "comments": [
    {
      "author": 2,
      "text": "Круто",
      "created_at": "2024-02-23T05:12:31.054234"
    }
  ],
  "likes_count": 20
}
```


## Критерии оценки

Зачёт по дипломной работе можно получить, если работа соответствует критериям:

* система реализована на Django версии 3 и выше,
* интерфейс администратора создан стандартными средствами Django admin,
* в качестве СУБД использован postgresql,
* реализованы все необходимые модели и сериализаторы,
* система при работе не должна вызывать исключения и ошибки,
* описана документация по запуску проекта.
