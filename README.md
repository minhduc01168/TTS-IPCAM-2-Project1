# TTS-IPCAM-2-Project1
## Một số khái niệm cơ bản
**Xử lý ảnh là gì?**

Con người thu nhận thông tin qua các giác quan, trong đó thị giác đóng vai trò quan trọng nhất. Những năm trở lại đây với sự phát triển của phần cứng máy tính, xử lý ảnh và đồ hoạ đó phát triển một cách mạnh mẽ và có nhiều ứng dụng trong cuộc sống. Xử lý ảnh và đồ hoạ đóng một vai trò quan trọng trong tương tác người máy. Quá trình xử lý ảnh được xem như là quá trình thao tác ảnh đầu vào nhằm cho ra kết quả mong muốn. Kết quả đầu ra của một quá trình xử lý ảnh có thể là một ảnh “tốt hơn” hoặc một kết luận.

**Ảnh và điểm ảnh**

- Đối tượng của xử lý ảnh là xử lý các ảnh tự nhiên, ảnh chụp, dữ liệu ảnh có nguồn gốc từ tín hiệu ảnh đặc trưng bởi biên độ và dải tần số. Có sự phân biệt giữa xử lý ảnh với đồ họa.
- Hệ thống xử lý ảnh thu nhận khung cảnh hoặc ảnh ở đầu vào, thực hiện các phép xử lý để tạo ra một ảnh ở đầu ra thỏa mãn các yêu cầu về cảm thụ hoặc trích rút các đặc trưng của ảnh.

**Hệ thống xử lý ảnh**

<a href="https://ibb.co/qYVpv0B"><p style="text-align:center;"><img src="https://i.ibb.co/VY5TsHV/Untitled.png" alt="Untitled" border="0"></p></a>

**Khử nhiễu:** Có 2 loại nhiễu cơ bản trong quá trình thu nhận ảnh

- Nhiều hệ thống: là nhiễu có quy luật có thể khử bằng các phép biến đổi
- Nhiễu ngẫu nhiên: vết bẩn không rõ nguyên nhân, khắc phục bằng các phép lọc

**Chỉnh mức xám**

- Nhằm khắc phục tính không đồng đều của hệ thống gây ra. Thông thường có 2 hướng tiếp cận:
- Giảm số mức xám: Thực hiện bằng cách nhóm các mức xám gần nhau thành một bó. Trường hợp chỉ có 2 mức xám thì chính là chuyển về ảnh đen trắng. Ứng dụng: In ảnh màu ra máy in đen trắng.
- Tăng số mức xám: Thực hiện nội suy ra các mức xám trung gian bằng kỹ thuật nội suy. Kỹ thuật này nhằm tăng cường độ mịn cho ảnh

**Trích chon đặc điểm**

- Đặc điểm không gian: Phân bố mức xám, phân bố xác suất, biên độ, điểm uốn v.v.. 
- Đặc điểm biến đổi: Các đặc điểm loại này được trích chọn bằng việc thực hiện lọc vùng (zonal filtering). Các bộ vùng được gọi là “mặt nạ đặc 10 điểm” (feature mask) thường là các khe hẹp với hình dạng khác nhau (chữ nhật, tam giác, cung tròn v.v..) 
- Đặc điểm biên và đường biên: Đặc trưng cho đường biên của đối tượng và do vậy rất hữu ích trong việc trích trọn các thuộc tính bất biến được dùng khi nhận dạng đối tượng. Các đặc điểm này có thể được trích chọn nhờ toán tử gradient, toán tử la bàn, toán tử Laplace, toán tử “chéo không” (zero crossing) v.v.. 

## Thuật toán Color Conversion

Không gian màu là một mô hình toán học dùng để mô tả các màu sắc trong thực tế được biểu diễn dưới dạng số học. Trên thực tế có rất nhiều không gian màu khác nhau được mô hình để sử dụng vào những mục đích khác nhau. Trong bài này ta sẽ tìm hiểu qua về ba không gian màu cơ bản hay được nhắc tới và ứng dụng nhiều, đó là hệ không gian màu RGB, HSV và CMYK.
- **RGB** là không gian màu rất phổ biến được dùng trong đồ họa máy tính và nhiều thiết bị kĩ thuật số khác. Ý tưởng chính của không gian màu này là sự kết hợp của 3 màu sắc cơ bản : màu đỏ (R, Red), xanh lục (G, Green) và xanh lơ (B, Blue) để mô tả tất cả các màu sắc khác.
- **CMYK** là không gian màu được sử dụng phổ biến trong ngành công nghiệp in ấn. Ý tưởng cơ bản của hệ không gian này là dùng 4 màu sắc cơ bản để phục vụ cho việc pha trộn mực in. Trên thực tế, người ta dùng 3 màu là C=Cyan: xanh lơ, M=Magenta: hồng xẫm, và Y=Yellow: vàng để biểu diễn các màu sắc khác nhau. Nếu lấy màu hồng xẫm cộng với vàng sẽ ra màu đỏ, màu xẫm kết hợp với xanh lơ sẽ cho xanh lam 
- **HSV** và cũng gần tương tự như HSL là không gian màu được dùng nhiều trong việc ch ỉnh sữa ảnh, phân tích ảnh và một phần của lĩnh vực thị giác máy tính. Hệ không gian này dựa vào 3 thông số sau để mô tả màu sắc H = Hue: màu sắc, S = Saturation: độ đậm đặc, sự bảo hòa, V = value: giá trị cường độ sáng.

### Chuyển đổi từ RGB sang CMYK và ngược lại

K là thành phần phụ dùng để in cho những điểm màu có màu đen trong hệ CYMK, do vậy để chuyển không gian màu từ RGB sang CMYK trước hết ta chuyển RGB sang CMY sau đó tìm thành phần K còn lại.
Công thức: $$(C', M', Y') = ((255 - R), (255 - G), (255 - B)) $$
Về mặt lý thuyết có thể chấp nhận $$K = min (C'/2,55, M'/2,55, Y'/2,55) $$

Ta có công thức
$$C = (C'/2.55 - K) * 100 /(100 - K)$$

$$M = (M'/2.55 - K) * 100 /(100 - K)$$

$$Y = (Y'/2.55 - K) *100 /(100 - K)$$

Trong đó, C, M, Y, K được làm tròn tới để lấy chỉ số nguyên.

## Background Subtraction

Background subtraction hay còn gọi là trừ nền là một trong những giải thuật đơn giản và phổ biến trong lĩnh vực Thị giác máy tính (Computer Vision). Thuật toán được sử dụng nhằm xác định đối tượng chuyển động trong camera nền tĩnh.

- Frame Difference

Ta sẽ tính hiệu giá trị pixel của khung hình hiện tại và khung hình trước đó nếu hiệu này lớn hơn ngưỡng **T** thì pixel tại vị trí đó thuộc về Foreground.

<a href="https://imgbb.com/"><p style="text-align:center;"><img src="https://i.ibb.co/KN2FRng/Untitled2.png" alt="Untitled2" border="0"></p></a>

**Ưu điểm** của phương pháp này là tốc độ tính toán nhanh do việc khởi tạo background image chỉ đơn giản là việc lấy khung hình trước đó.

**Nhược điểm** của phương pháp này là nó chỉ tốt với những đối tượng di chuyển liên tục nhưng khi có một đối tượng đứng yên trong khung hình quá lâu thì đối tượng này sẽ bị cho là background cùng với đó phương pháp này phụ thuộc rất nhiều vào ngưỡng T do đó với mỗi video ta đều phải chọn 1 ngưỡng phù hợp.

<a href="https://imgbb.com/"><p style="text-align:center;"><img src="https://i.ibb.co/bjhbHvK/Untitled3.png" alt="Untitled3" border="0"></p></a>

- Mean Filter

Thay vì chỉ sử dụng 1 khung hình trước đó để làm background image thì Mean Filter sử dụng **N** khung hình phía trước khung hình đang xét để khởi tạo background image. Giả sử khung hình đang xét tại thời điểm t thì background tương ứng với nó sẽ được tính như sau:

<a href="https://imgbb.com/"><p style="text-align:center;"><img src="https://i.ibb.co/1XN9dk8/Untitled4.png" alt="Untitled4" border="0"></p></a>

Trong đó B là background image tại thời điểm t, N là số khung hình trước thời điểm t để dùng cho việc tính toán ra background image, $I(x, y, t)$ là khung hình tại thời điểm t. Sau khi khởi tạo background image thì phần còn lại của phương pháp này cũng giống với phương pháp frame difference.

## Erosion

Erosion hay còn gọi là xói mòn là một trong hai toán tử cơ bản trong lĩnh vực hình thái toán học (mathematical morphology). Nó thường được áp dụng trong những hình ảnh nhị phân tuy nhiên có một số phiên bản sẽ được áp dụng trên những hình ảnh xám tuy nhiên trong phạm vi bài viết của mình hôm nay thì chỉ tập trung vào những hình ảnh nhị phân.

<img src="https://tapit.vn/wp-content/uploads/2021/11/10.gif" alt="erosion" />

Mục đích của phương pháp này sẽ giúp:
- Loại bỏ những pixel nhiễu cô lập
- Loại bỏ những pixel nhiễu xung quanh đối tượng giúp cho phần viền (cạnh) của đối tượng trở nên mịn hơn
- Loại bỏ lớp viền (cạnh) của đối tượng giúp đối tượng trở nên nhỏ hơn và đặt những pixel viền đó trở thành lớp nền của đối tượng




