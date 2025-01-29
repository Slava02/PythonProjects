# Работа с утилитой screen

## Установка screen в Ubuntu

```bash
sudo apt-get install screen
```

## Основные команды

### Задать имя сессии

```bash
screen -S MY_SCREEN_1
```

### Свернуть или выйти из сессии 

Нажмите `Ctrl+Shift+a`, затем `d`.

### Список сессий

```bash
screen -ls
```

**Пример результата выполнения команды:**
```shell
There are screens on:
18148.MY_SCREEN_1 (02/11/23 06:06:06)
```

### Вернуться к последней подключенной сессии

```bash
screen -r
```

*(Detached)*

### Перейти в нужную сессию

Укажите параметру `-r` её id или название:

```bash
screen -r 18148
```

или

```bash
screen -r MY_SCREEN_1
```

## Запуск процессов

### Запуск процесса в фоновом режиме

```bash
screen -S MY_SCREEN_2 ping mail.ru
```

### Запуск процесса в новой сессии в фоновом режиме

```bash
screen -dmS MY_SCREEN_3 ping mail.ru
```

---

## Дополнительная информация

1. [Применение утилиты screen на практике](https://losst.pro/komanda-screen-linux)
2. [Основные консольные команды](https://codex.so/screen)