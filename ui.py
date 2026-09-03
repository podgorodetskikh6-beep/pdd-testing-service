from tkinter import *
from core.test import TestService
from PIL import Image,ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

class UI:
    def __init__(self, exam_factory, user_service, stats_service):
        self.exam_factory = exam_factory
        self.user_service = user_service
        self.stats_service = stats_service
        self.current_user = None
        self.exam = None
        self.root = Tk()
        self.root.title("Тест ПДД")
        self.root.geometry("700x900")
        self.root.configure(bg='#EEF2F7')
        self.header_label = Label(self.root, text="", bg='#EEF2F7')
        self.header_label.pack(pady=5)
        self.current_window = self.root
        self.show_login()

    def show_login(self):
        self.clear_screen()

        Label(self.root, text="Введите имя пользователя:",bg='azure').pack(pady=10)

        self.username_entry = Entry(self.root, width=30)
        self.username_entry.pack(pady=10)

        Button(
            self.root,
            text="Войти / Зарегистрироваться",
            command=self.login_user
        ).pack(pady=10)

    def login_user(self):
        username = self.username_entry.get().strip()

        if not username:
            return

        self.current_user = self.user_service.create_user(username)

        self.header_label.config(text=f"Пользователь: {username}",bg='azure')
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_screen()
        Button(
            self.root,
            text="Моя статистика",
            width=30,
            command=self.show_stats,
            bg='azure'
        ).pack(pady=10)


        ticket_ids = self.exam_factory.get_ticket_ids()

        for ticket_id in ticket_ids:
            Button(
                self.root,
                text=f"Билет {ticket_id}",
                width=30,
                command=lambda t=ticket_id: self.start_test(t)
            ).pack(pady=5)

    def show_stats(self):
        self.clear_screen()
        stats = self.stats_service.get_stats(self.current_user)
        Label(self.root, text="Статистика", font=("Arial", 14), bg='azure').pack(pady=10)
        if not stats:
            Label(self.root, text="Пока нет результатов", bg='azure').pack(pady=10)
            Button(
                self.root,
                text="Назад",
                command=self.show_main_menu
            ).pack(pady=10)
            return

        container = Frame(self.root)
        container.pack(fill="both", expand=True)
        canvas = Canvas(container, highlightthickness=0, bd=0)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = Frame(canvas, bd=0)
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tickets = {}
        for s in stats:
            ticket_id = s["ticket_id"]
            tickets.setdefault(ticket_id, []).append(s)

        for ticket_id, attempts in tickets.items():
            attempts = sorted(attempts, key=lambda a: a["id"])
            x = list(range(1, len(attempts) + 1))
            y = [a["correct_answers"] for a in attempts]
            fig = Figure(figsize=(6, 3), dpi=100, constrained_layout=True)
            ax = fig.add_subplot(111)
            ax.plot(x, y, marker="o")
            ax.set_title(f"Билет {ticket_id} — попытки")
            ax.set_xlabel("Попытка")
            ax.set_ylabel("Правильные ответы")
            ax.set_xticks(x)
            ax.set_ylim(0, max(y) + 1)
            canvas_fig = FigureCanvasTkAgg(fig, master=scroll_frame)
            canvas_fig.draw()
            canvas_fig.get_tk_widget().pack(pady=15)

        grouped = defaultdict(list)
        for s in stats:
            grouped[s["ticket_id"]].append(s["correct_answers"])
        ticket_ids = []
        averages = []

        for t_id, values in grouped.items():
            ticket_ids.append(t_id)
            averages.append(sum(values) / len(values))
        fig = Figure(figsize=(6, 3), dpi=100, constrained_layout=True)
        ax = fig.add_subplot(111)
        ax.bar(ticket_ids, averages)
        ax.set_title("Средний результат по билетам")
        ax.set_xlabel("Билет")
        ax.set_ylabel("Среднее количество правильных")
        ax.set_xticks(ticket_ids)
        canvas_fig = FigureCanvasTkAgg(fig, master=scroll_frame)
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(pady=15)
        Button(
            self.root,
            text="Назад",
            command=self.show_main_menu
        ).pack(pady=20)
        self.root.update_idletasks()

    def start_test(self, ticket_id):
        ticket = self.exam_factory.get_ticket(ticket_id)
        self.exam = TestService(ticket)

        self.clear_screen()
        self.current_window = self.root

        self.label = Label(self.root, text="", wraplength=450, justify="left",bg='azure')
        self.label.pack(pady=20)
        self.image_label = Label(self.root)
        self.image_label.pack(pady=10)

        self.buttons_frame = Frame(self.root)
        self.buttons_frame.pack()

        self.update_question()

    def update_question(self):
        if self.exam.is_finished():
            result = self.exam.result()
            self.stats_service.save_result(
                user_id=self.current_user,
                ticket_id=result["ticket"],
                correct=result["correct"],
                total=result["total"]
            )
            self.clear_buttons()
            reason = self.exam.finish_reason()
            self.label.config(
                text=(
                    f"Тест заверешен\n\n"
                    f"Билет: {result['ticket']}\n"
                    f"Правильных ответов: {result['correct']}\n"
                    f"Ошибок: {result['errors']}\n"
                    f"Всего вопросов в тесте: {result['total']}\n\n"
                    f"Причина завершения:\n{reason}"
                ), bg='azure'
            )
            result = self.exam.result()

            errors = result.get("error_details", [])

            if errors:
                error_text = "\n\nОшибки:\n\n"

                for i, e in enumerate(errors, 1):
                    error_text += (
                        f"{i}. {e['text']}\n"
                        f"   Ваш ответ: {e['your']}\n"
                        f"   Правильный: {e['correct']}\n\n"
                    )

                error_label = Label(
                    self.root,
                    text=error_text,
                    justify="left",
                    wraplength=650,
                    bg='azure'
                )
                error_label.pack(pady=10)
            back_btn = Button(
                self.buttons_frame,
                text="Выбрать другой билет",
                width=30,
                command=self.back_to_tickets
            )
            back_btn.pack(pady=10)
            self.image_label.config(image="")

            return

        q = self.exam.get_current_question()
        image_path = getattr(q, "image_path", None)

        current, total = self.exam.get_progress()

        self.label.config(
            text=f"Вопрос {current}/{total}\n\n{q.text}",bg='azure'
        )

        if image_path:
            try:
                image = Image.open(image_path)
                image = image.resize((350, 250))
                self.photo = ImageTk.PhotoImage(image)

                self.image_label.config(image=self.photo)
            except Exception as e:
                print("Ошибка загрузки картинки:", e)
                self.image_label.config(image="")
        else:
            self.image_label.config(image="")
        self.clear_buttons()

        for variant in q.variants:
            Button(
                self.buttons_frame,
                text=variant,
                wraplength=400,
                width=50,
                command=lambda v=variant: self.submit(v)
            ).pack(pady=5)

    def submit(self, answer):
        self.exam.answer(answer)
        self.update_question()

    def back_to_tickets(self):
        self.exam = None
        self.clear_buttons()
        if hasattr(self, "image_label"):
            self.image_label.config(image="")
        self.show_main_menu()

    def clear_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            if widget != self.header_label:
                widget.destroy()

    def run(self):
        self.root.mainloop()