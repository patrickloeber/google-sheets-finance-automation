import sheets_utility as su
from data_loader import get_data


if __name__ == "__main__":
    service = su.create_authorized_service()
    # su.create_sheet(service)

    sid = "YOUR SPREADSHEET ID"

    data = get_data()

    su.update_values(service, sid, data)
    su.format_cells(service, sid, 0)
    su.create_pivot_table(service, sid, 0, data)

    print("Created sheets data successfully")
