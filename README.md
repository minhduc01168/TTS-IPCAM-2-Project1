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
## **Phép toán mở (Opening)**
Thực hiện phép co (Erosion) trước sau đó mới thực hiện phép giãn nở (Dilation). 

**Công thức**

![image](https://user-images.githubusercontent.com/81012512/185522131-7b063ff5-3499-4fe3-a165-21b57f178c64.png)

**Ứng dụng:**
Phép toán mở (Opening) được ứng dụng trong việc loại bỏ các phần lồi lõm và làm cho đường bao các đối tượng trong ảnh trở nên mượt mà hơn.

Sử dụng hàm cv.morphologyEx() trong OpenCV với đối số cv.MORPH_OPEN

## **Phép toán đóng (Closing)**
Thực hiện phép giãn nở (Dilation) trước sau đó mới thực hiện phép co (Erosion). 

**Công thức**

![image](https://user-images.githubusercontent.com/81012512/185522317-d2052812-9c22-4602-8d69-eef81e407b7e.png)

**Ứng dụng:**
Phép toán đóng (Closing) được dùng trong ứng dụng làm trơn đường bao các đối tượng, lấp đầy các khoảng trống biên và loại bỏ những hố nhỏ.

Sử dụng hàm cv.morphologyEx() trong OpenCV với đối số cv.MORPH_CLOSE

## **Một số thuật toán tracking**
1. Boosting

    Trình theo dõi này chậm và không hoạt động tốt.

2. MIL (Multiple Instance Learning)
    Tốt hơn Boosting nhưng kém trong việc báo cáo lỗi.

3. KCF (Kernel Correlation Filters)

    Nhanh hơn Boosting và MIL. Nhưng tương tự MIL không xử lý tốt tình trạng tắc hoàn toàn.

4. CSRT (Discriminative Correlation Filter với Channel và Spatial Reliability)

    Có xu hướng chính xác hơn KCF nhưng chậm hơn một chút.

5. MedianFlow

    Nếu có quá nhiều bước nhảy trong chuyển động, chẳng hạn như các đối tượng di chuyển nhanh hoặc các đối tượng thay đổi nhanh chóng về ngoại hình của chúng, mô hình     sẽ thất bại.

6. TLD (Tracking Learning Detection)

    TLD dễ bị sai đối với các vật giả. Không nên sử dụng TLD với OpenCV 

7. MOSSE (Minimum Output Sum of Squared) Error)

    Rất, rất nhanh. Không chính xác như CSRT hoặc KCF nhưng là một lựa chọn tốt nếu cần tốc độ.

8. Goturn (Generic Object Tracking Using Regression Networks)

    Phát hiện dối tượng dựa trên deeplearning

9. Meanshift
    Dựa vào thuật toán phân cụm KMean 

10. CAMShift (Continuously Adaptive Meanshift)

    Camshift gần giống như meanhift, chỉ khác là trả về một hình chữ nhật xoay và các tham số được sử dụng để chuyển làm cửa sổ tìm kiếm trong lần lặp tiếp theo.

11. Optical Flow Sparse 

    Ước tính vectơ dịch chuyển của đối tượng gây ra bởi chuyển động hoặc chuyển động của máy ảnh.
    
12. Optical Flow Dense

**Đề xuất cá nhân:**

Sử dụng CSRT khi bạn cần độ chính xác theo dõi đối tượng cao hơn và có thể chịu được thông lượng FPS chậm hơn.

Sử dụng KCF khi bạn cần thông lượng FPS nhanh hơn nhưng có thể xử lý độ chính xác theo dõi đối tượng thấp hơn một chút.

Sử dụng MOSSE khi bạn cần tốc độ thuần.

