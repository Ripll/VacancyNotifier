class VacancyMsg:
    @staticmethod
    def def_msg(item) -> str:
        msg = f"<b>{item.title}</b>\n" \
              f"<i>{item.company}</i> - {item.city}  <b>{a if (a := item.salary) else ''}</b>\n\n" \
              f"{item.desc}\n" \
              f"<a href='{item.link}'>Откликнуться</a>"
        return msg
