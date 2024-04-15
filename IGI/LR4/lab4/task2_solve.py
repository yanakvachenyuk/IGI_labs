from TextAnalyzer import TextAnalyzer
import zipfile
from datetime import datetime
def task2_solve():
    """Main function for task 2."""

    input_file = 'task2_input.txt'
    output_file = 'task2_output.txt'
    archive_file = 'task2_archive.zip'
    text_analyzer = TextAnalyzer(input_file, output_file, archive_file)
    text_analyzer.load_text()
    text_analyzer.analyze_text()
    text_analyzer.save_results()
    text_analyzer.archive_results()
    print()
    with zipfile.ZipFile('task2_archive.zip', 'r') as myzip:
        for info in myzip.infolist():
            print(info.filename)
            print('Размер файла:', info.file_size, 'байт')
            print('Размер сжатого файла:', info.compress_size, 'байт')
            print("Тип сжатия:", info.compress_type)
            date_time = datetime(*info.date_time)
            print("Дата создания:", date_time.isoformat())
