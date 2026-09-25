import codecs

path = 'd:/งานมด/duty-app/src/app/report/page.tsx'

with codecs.open(path, 'r', 'utf-8') as f:
    c = f.read()

import_statement = "import Cropper from 'react-easy-crop';\n"
c = c.replace('import { useRouter } from "next/navigation";', 'import { useRouter } from "next/navigation";\n' + import_statement)

states = """  // Crop states
  const [rawPhoto, setRawPhoto] = useState<string | null>(null);
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState<any>(null);
"""
c = c.replace('  // Friends present', states + '  // Friends present')

old_capture = """  const handlePhotoCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const img = new window.Image();
        img.onload = () => {
          const canvas = document.createElement("canvas");
          const MAX_WIDTH = 800;
          const MAX_HEIGHT = 800;
          let width = img.width;
          let height = img.height;

          if (width > height) {
            if (width > MAX_WIDTH) {
              height *= MAX_WIDTH / width;
              width = MAX_WIDTH;
            }
          } else {
            if (height > MAX_HEIGHT) {
              width *= MAX_HEIGHT / height;
              height = MAX_HEIGHT;
            }
          }
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext("2d");
          ctx?.drawImage(img, 0, 0, width, height);
          
          // บีบอัดภาพให้อยู่ในลิมิต Google Sheets
          const compressedDataUrl = canvas.toDataURL("image/jpeg", 0.6);
          setPhoto(compressedDataUrl);
        };
        img.src = event.target?.result as string;
      };
      reader.readAsDataURL(file);
    }
  };"""

new_capture = """  const handlePhotoCapture = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Just load the raw file into state first, cropper UI will handle the rest
      const reader = new FileReader();
      reader.onload = (event) => {
        setRawPhoto(event.target?.result as string);
        setPhoto(null); // Clear previous photo
        setCrop({ x: 0, y: 0 }); // Reset crop
        setZoom(1); // Reset zoom
      };
      reader.readAsDataURL(file);
    }
    // clear input value so picking the same file works again
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleCropConfirm = async () => {
    if (!rawPhoto || !croppedAreaPixels) return;

    try {
      const image = new window.Image();
      image.src = rawPhoto;
      await new Promise((resolve, reject) => {
        image.onload = resolve;
        image.onerror = reject;
      });

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      canvas.width = croppedAreaPixels.width;
      canvas.height = croppedAreaPixels.height;

      ctx.drawImage(
        image,
        croppedAreaPixels.x,
        croppedAreaPixels.y,
        croppedAreaPixels.width,
        croppedAreaPixels.height,
        0,
        0,
        croppedAreaPixels.width,
        croppedAreaPixels.height
      );

      // Now compress and resize the cropped canvas
      const MAX = 800;
      let finalWidth = canvas.width;
      let finalHeight = canvas.height;

      if (finalWidth > MAX || finalHeight > MAX) {
        if (finalWidth > finalHeight) {
          finalHeight *= MAX / finalWidth;
          finalWidth = MAX;
        } else {
          finalWidth *= MAX / finalHeight;
          finalHeight = MAX;
        }
      }

      const resizedCanvas = document.createElement('canvas');
      resizedCanvas.width = finalWidth;
      resizedCanvas.height = finalHeight;
      const resCtx = resizedCanvas.getContext('2d');
      resCtx?.drawImage(canvas, 0, 0, finalWidth, finalHeight);

      const compressedUrl = resizedCanvas.toDataURL('image/jpeg', 0.6);
      setPhoto(compressedUrl);
      setRawPhoto(null); // Hide cropper
    } catch (e) {
      console.error(e);
      alert("เกิดข้อผิดพลาดในการตัดรูปภาพ");
    }
  };"""

c = c.replace(old_capture, new_capture)

cropper_ui = """        {/* Cropper Modal */}
        {rawPhoto && !photo && (
          <div className="fixed inset-0 z-[100] bg-black flex flex-col">
            <div className="flex-1 relative">
              <Cropper
                image={rawPhoto}
                crop={crop}
                zoom={zoom}
                aspect={4 / 3}
                onCropChange={setCrop}
                onCropComplete={(_, croppedAreaPixels) => setCroppedAreaPixels(croppedAreaPixels)}
                onZoomChange={setZoom}
              />
            </div>
            <div className="bg-gray-900 p-6 pb-12 flex flex-col gap-6 rounded-t-3xl shadow-2xl z-10">
              <div className="text-center">
                <p className="text-white font-medium">จัดวางรูปภาพให้อยู่ในกรอบ</p>
                <p className="text-gray-400 text-sm mt-1">สามารถเลื่อนและซูมเข้า-ออกได้</p>
              </div>
              <div className="flex gap-4 max-w-sm mx-auto w-full">
                <button
                  type="button"
                  onClick={() => setRawPhoto(null)}
                  className="flex-1 bg-gray-700 hover:bg-gray-600 text-white font-medium py-3 rounded-xl transition-colors"
                >
                  ยกเลิก
                </button>
                <button
                  type="button"
                  onClick={handleCropConfirm}
                  className="flex-1 bg-indigo-500 hover:bg-indigo-600 text-white font-medium py-3 rounded-xl transition-colors shadow-lg shadow-indigo-500/30"
                >
                  ยืนยันรูปภาพ
                </button>
              </div>
            </div>
          </div>
        )}"""

c = c.replace('{/* รูปถ่าย Section */}', cropper_ui + '\n\n        {/* รูปถ่าย Section */}')

with codecs.open(path, 'w', 'utf-8') as f:
    f.write(c)

print('Updated report page with cropper!')
