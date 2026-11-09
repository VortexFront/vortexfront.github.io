# Максим Асатуров · Fullstack portfolio

**Портфолио:** https://vortexfront.github.io/

**Контакт:** volckovna@gmail.com

Самостоятельно разрабатываю корпоративные веб-приложения, backend, API, AI-интеграции и сервисы автоматизации. В портфолио показываю, какие задачи решают приложения, как они работают и что я реализовал.

## Проекты

Пять подробных кейсов: Staff Suite, Campaign Control, Loyalty Platform, Events Platform и CRM–Sheets Sync. Для каждого описаны возможности сервиса, моя разработка, технические решения и результаты. Библиотека содержит ещё 17 работ с назначением и стеком.

Публичные названия согласованы с каталогом проектов: Staff Suite — `nextstaff`, Campaign Control — `target-control-center`, Loyalty Platform — `friends-loyalty`, Events Platform — `next-afisha`, CRM–Sheets Sync — `bitrix-sheets-automation`.

## Актуальное резюме

Обновлено 9 ноября 2026. В PDF и Word описаны самостоятельно разработанные проекты; обе версии содержат ссылку на портфолио.

- [Скачать PDF](https://vortexfront.github.io/assets/resume-maxim-asaturov-2026-11-09.pdf)
- [Скачать Word](https://vortexfront.github.io/assets/resume-maxim-asaturov-2026-11-09.docx)

Текст хранится в `resume.md`. PDF и Word собираются из одного источника командой `python scripts/build_resume.py`; нужны `python-docx`, `reportlab` и шрифты Arial. Старый адрес Word сохранён как совместимый адрес актуального файла.

## Запуск и публикация

HTML, CSS и обычный JavaScript, без npm, сборщика и внешних шрифтов. Для локального просмотра:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

GitHub Pages публикует корень ветки `main`; изменения этой ветки автоматически обновляют сайт. `.nojekyll` сохраняет готовые статические файлы без обработки Jekyll.

Разметка `index.html` и сведения `showcase-data.json` должны оставаться согласованными. Поиск и фильтры библиотеки, галерея и навигация работают без сторонних библиотек; без JavaScript все 17 записей остаются доступны.

Снимки показывают локальные приложения на синтетических данных. Статическая страница не размещает backend сервисов, не подключается к рабочим CRM и платежам и не открывает административный доступ. Технические границы демонстраций описаны внутри кейсов.
