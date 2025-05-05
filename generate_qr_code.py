import qrcode

object_ids = ["s1", "moon", "gl-m", "dogs", "m76"]


for obj_id in object_ids:
    deep_link = f"https://t.me/QRSpaceBot?start={obj_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(deep_link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"qr_{obj_id}.png")
    print(f"QR-код для объекта {obj_id} создан: qr_{obj_id}.png")