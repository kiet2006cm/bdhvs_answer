import json
import os

DESTINATION_FOLDER = r'D:\tool\binhdanhocvuso\bdhvs_answer'
DESTINATION_FILE = r'moc02.json'


def remove_duplicates(root_folder: str = DESTINATION_FOLDER, file_name: str = DESTINATION_FILE, ask_to_overwrite: bool = True) -> None:
    json_file = os.path.join(root_folder, file_name)
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Lỗi khi đọc file {json_file}: {e}")
        return

    print(f"\n📂 Đang xử lý file: {json_file}")
    print(f"Bắt đầu quá trình lọc các duplicates giống hệt...\n")
    
    seen_signatures = set()
    unique_list = []
    removed_duplicates_log = []

    for current_item in data:
        # Tạo một "chữ ký" duy nhất cho mỗi item dựa trên cả Q_ID và Answer
        # Tuple là một cấu trúc hashable nên có thể thêm vào set
        # Sử dụng .get() để tránh lỗi nếu key 'Answer' không tồn tại
        signature = (current_item.get('Q_ID'), current_item.get('Answer'))

        if signature in seen_signatures:
            # Nếu đã thấy chữ ký này, nó là một duplicate hoàn toàn
            print(f"🗑️  [Q_ID: {current_item.get('Q_ID')}] Duplicate giống hệt đã bị loại bỏ: {current_item}")
            removed_duplicates_log.append(current_item)
        else:
            # Nếu chưa thấy, thêm nó vào danh sách kết quả và ghi nhớ chữ ký
            unique_list.append(current_item)
            seen_signatures.add(signature)
            
    # ================= LOGIC MỚI KẾT THÚC TẠI ĐÂY =================

    print("\n-------------------------------------------")
    print("\n✅ Quá trình lọc hoàn tất!")

    if not removed_duplicates_log:
        print("Không tìm thấy duplicate nào để loại bỏ.")
    else:
        print("\nDanh sách các duplicates đã bị loại bỏ:")
        for log_item in removed_duplicates_log:
            print(f"- {log_item}")
    
    # Kiểm tra xem có sự thay đổi nào không trước khi hỏi ghi đè
    if len(data) == len(unique_list):
        print("\nKhông có gì thay đổi, file gốc được giữ nguyên.")
        return

    if ask_to_overwrite:
        # Sửa lỗi logic input: w.lower() != 'y' AND w != ''
        w = input(f"\nBạn có muốn ghi đè file gốc với {len(unique_list)} bản ghi duy nhất không? (Y/n): ").lower()
        if w not in ('y', ''):
            print("Hủy ghi đè file gốc.")
            return

    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(unique_list, f, indent=4, ensure_ascii=False)
        print(f"Đã ghi dữ liệu đã lọc vào file: {json_file}")
    except IOError as e:
        print(f"Lỗi khi ghi file: {e}")


def severals_files(root_folder: str = DESTINATION_FOLDER) -> None:
    for file_name in os.listdir(root_folder):
        if file_name.endswith('.json'):
            remove_duplicates(root_folder, file_name, ask_to_overwrite=False) # Thêm ask_to_overwrite=False để chạy hàng loạt

if __name__ == '__main__':
    remove_duplicates()
    # Hoặc chạy cho tất cả các file trong thư mục:
    # severals_files()