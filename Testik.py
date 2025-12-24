import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton,
                             QComboBox, QGridLayout, QGroupBox, QMessageBox)


class AgriculturalCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.product_data = {
            "ячмень": {"арендная_плата": 1500, "договорные_обязательства": 50000},
            "пшеница": {"арендная_плата": 1200, "договорные_обязательства": 25000},
            "подсолнечник": {"арендная_плата": 1800, "договорные_обязательства": 32000}
        }
        self.chart_window = None  # Храним ссылку на окно диаграммы
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Сельскохозяйственный калькулятор")
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ВВОД ДАННЫХ
        input_group = QGroupBox("Ввод данных")
        input_layout = QGridLayout()

        input_layout.addWidget(QLabel("Тип продукции:"), 0, 0)
        self.product_combo = QComboBox()
        self.product_combo.addItems(["ячмень", "пшеница", "подсолнечник"])
        self.product_combo.currentTextChanged.connect(self.update_contract)
        input_layout.addWidget(self.product_combo, 0, 1)

        input_layout.addWidget(QLabel("Численность работников:"), 1, 0)
        self.workers_edit = QLineEdit()
        input_layout.addWidget(self.workers_edit, 1, 1)

        input_layout.addWidget(QLabel("Количество животных:"), 2, 0)
        self.animals_edit = QLineEdit()
        input_layout.addWidget(self.animals_edit, 2, 1)

        input_layout.addWidget(QLabel("Норматив корма на 1 гол:"), 3, 0)
        self.feed_edit = QLineEdit()
        input_layout.addWidget(self.feed_edit, 3, 1)

        input_layout.addWidget(QLabel("Договорные обязательства:"), 4, 0)
        self.contract_label = QLabel("0")
        input_layout.addWidget(self.contract_label, 4, 1)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # КНОПКИ
        buttons_layout = QHBoxLayout()

        self.btn_rent = QPushButton("Плата за паи")
        self.btn_rent.clicked.connect(self.calc_rent)
        buttons_layout.addWidget(self.btn_rent)

        self.btn_livestock = QPushButton("Потребность животноводства")
        self.btn_livestock.clicked.connect(self.calc_livestock)
        buttons_layout.addWidget(self.btn_livestock)

        self.btn_total = QPushButton("Итоговая потребность")
        self.btn_total.clicked.connect(self.calc_total)
        buttons_layout.addWidget(self.btn_total)

        self.btn_chart = QPushButton("Диаграмма")
        self.btn_chart.clicked.connect(self.show_chart)
        buttons_layout.addWidget(self.btn_chart)

        main_layout.addLayout(buttons_layout)

        # РЕЗУЛЬТАТЫ
        result_group = QGroupBox("Результаты")
        result_layout = QGridLayout()

        result_layout.addWidget(QLabel("Плата за паи:"), 0, 0)
        self.result_rent = QLabel("0")
        result_layout.addWidget(self.result_rent, 0, 1)

        result_layout.addWidget(QLabel("Потребность животноводства:"), 1, 0)
        self.result_livestock = QLabel("0")
        result_layout.addWidget(self.result_livestock, 1, 1)

        result_layout.addWidget(QLabel("Итоговая потребность:"), 2, 0)
        self.result_total = QLabel("0")
        result_layout.addWidget(self.result_total, 2, 1)

        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

        # Кнопка арендной платы
        self.btn_show_rent = QPushButton("Показать арендную плату")
        self.btn_show_rent.clicked.connect(self.show_rent_info)
        main_layout.addWidget(self.btn_show_rent)

        # Обновляем договорные обязательства
        self.update_contract()

    def update_contract(self):
        product = self.product_combo.currentText()
        if product in self.product_data:
            value = self.product_data[product]["договорные_обязательства"]
            self.contract_label.setText(str(value))

    def show_rent_info(self):
        product = self.product_combo.currentText()
        if product in self.product_data:
            rent = self.product_data[product]["арендная_плата"]
            QMessageBox.information(self, "Арендная плата", f"Для {product}: {rent}")

    def get_number(self, text, field_name):
        try:
            num = float(text)
            if num < 0:
                QMessageBox.warning(self, f"{field_name} не может быть отрицательным")
                return None
            return num
        except ValueError:
            QMessageBox.warning(self, f"Введите число для {field_name}")
            return None

    def calc_rent(self):
        workers = self.get_number(self.workers_edit.text(), "Численность работников")
        if workers is None:
            return

        product = self.product_combo.currentText()
        rent_price = self.product_data[product]["арендная_плата"]

        result = workers * rent_price
        self.result_rent.setText(f"{result:.2f}")

    def calc_livestock(self):
        animals = self.get_number(self.animals_edit.text(), "Количество животных")
        if animals is None:
            return

        feed = self.get_number(self.feed_edit.text(), "Норматив корма")
        if feed is None:
            return

        result = animals * feed
        self.result_livestock.setText(f"{result:.2f}")

    def calc_total(self):
        rent_text = self.result_rent.text()
        livestock_text = self.result_livestock.text()
        contract_text = self.contract_label.text()

        if rent_text == "0" or livestock_text == "0":
            QMessageBox.warning(self, "Сначала необходимо выполнить расчеты")
            return

        try:
            rent = float(rent_text)
            livestock = float(livestock_text)
            contract = float(contract_text)

            total = rent + livestock + contract
            self.result_total.setText(f"{total:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Ошибка при расчете")

    def show_chart(self):
        """Создание и отображение круговой диаграммы"""
        try:
            # Получаем значения
            rent_text = self.result_rent.text()
            livestock_text = self.result_livestock.text()
            contract_text = self.contract_label.text()

            # Проверяем, что есть данные для диаграммы
            if rent_text == "0" and livestock_text == "0":
                QMessageBox.warning(self, "Нет данных для диаграммы.\nСначала выполните расчеты!")
                return

            # Преобразуем в числа
            rent = float(rent_text)
            livestock = float(livestock_text)
            contract = float(contract_text)

            # Закрываем предыдущее окно диаграммы, если оно открыто
            if self.chart_window is not None:
                self.chart_window.close()

            # Создаем новое окно для диаграммы
            self.chart_window = QWidget()
            self.chart_window.setWindowTitle(f"Диаграмма - {self.product_combo.currentText()}")
            self.chart_window.setGeometry(200, 200, 600, 500)

            layout = QVBoxLayout(self.chart_window)

            # Создаем фигуру matplotlib
            fig, ax = plt.subplots(figsize=(6, 5))

            # Данные для диаграммы
            labels = ['Плата за паи', 'Животноводство', 'Договор']
            values = [rent, livestock, contract]
            colors = ['#66b3ff', '#99ff99', '#ff9999']

            # Рисуем диаграмму
            wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors,
                                              autopct='%1.1f%%', startangle=90)

            # Настраиваем внешний вид
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')

            ax.set_title(f'Распределение потребности\n({self.product_combo.currentText()})',
                         fontsize=14, fontweight='bold')

            # Добавляем легенду
            ax.legend(wedges, [f'{label}: {value:.2f} ц' for label, value in zip(labels, values)],
                      title="Значения", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

            # Добавляем диаграмму в окно
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)

            # Добавляем кнопку закрытия
            close_btn = QPushButton("Закрыть")
            close_btn.clicked.connect(self.chart_window.close)
            layout.addWidget(close_btn)

            # Показываем окно
            self.chart_window.show()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать диаграмму:\n{str(e)}")


def main():
    app = QApplication(sys.argv)
    window = AgriculturalCalculator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()