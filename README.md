# TTS-IPCAM-2-Project1
## Tìm hiểu video 
Một video kỹ thuật số là một chuỗi các hình ảnh kỹ thuật dược hiển thị ở một tốc độ nhất định( khung hình trên giây )
![image](https://user-images.githubusercontent.com/81012512/185344918-8c8599f4-5579-424b-b7e5-ffbf6326b701.png)

Khung hình trên giây (fps) của vieo là đại lượng của số khung hình xuất hiện trong một giây của video đó. FPS càng cao thì hình ảnh sẽ mượt. Trong thực tế, tố độ 25-30 fps là tốc độ chuẩn thường được sử dụng nhất ( phim ảnh, truyền hình,..) đủ để hình ảnh mượt mà không gây mỏi mát.

Với tốc độ cao hơn, có thể tạo được hiệu ứng quay chậm như slowmotion, được sử dụng để quay các đối tượng có vận tốc di chuyển nhanh, cần độ chính xác. Còn đối với các hệ thống camera giám sát thì tốc độ này thường sẽ thấp vì để giảm dung lượng lưu trữ và truyền tải.

**Chuẩn mã hóa: MPEG2, MPEG4, H264,...**

## Thuật toán cơ bản: Denoise 
**Mục đích:** Loại/xóa nhiễu khỏi hình ảnh. Sử dụng khi nhiễu không chỉ chịu ảnh hưởng của khu vực lân cận.

**Ý tưởng:** Xem xét một pixel nhiễu p = p + n trong đó p là giá trị pixel và n là nhiễu. Giả sử xem xét cùng một pixel từ các khung khác nhau (nghĩa là, nếu chúng ta giữ máy ảnh tĩnh và chụp một chủ đề nhất định trong vài giây trong video, chúng ta có thể nhận được các khung khác nhau) của cùng một hình ảnh và tính trung bình. Sau đó, ta có thể thu được p = p, n = 0. Nhưng không dễ dàng có các khung khác nhau của cùng một hình ảnh. Trong trường hợp này, ta có thể xem xét các khu vực tương tự trong cùng một hình ảnh bằng cửa sổ 5 x 5 hoặc 7 x 7 và tìm mức trung bình của chúng.
    
     Hàm cv.fastNlMeansDenoising() sử dụng cho ảnh xám. 
     
     Hàm cv.fastNlMeansDenoisingColored() sử dụng cho ảnh màu.
