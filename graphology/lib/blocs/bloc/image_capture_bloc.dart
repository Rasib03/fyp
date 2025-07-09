import 'package:bloc/bloc.dart';
import 'package:image_picker/image_picker.dart';
import 'package:meta/meta.dart';

part 'image_capture_event.dart';
part 'image_capture_state.dart';

class ImageCaptureBloc extends Bloc<ImageCaptureEvent, ImageCaptureState> {
  ImageCaptureBloc() : super(ImageCaptureInitial()) {
    on<ImageCaptureEvent>((event, emit) {});

    on<ImageCaptureRequest>((event, emit) {
      emit(OpenCameraScreen());
    });

    on<ImageCapturedEvent>((event, emit) {
      if (event.image != null) {
        emit(ImageCapturedState(image: event.image));
      } else {
        emit(ImageCaptureInitial());
      }
    });

    on<ImageGalleryRequest>((event, emit) async {
      final _pickedImage = await ImagePicker().pickImage(
        source: ImageSource.gallery,
      );

      emit(ImageGalleryPicked(image: _pickedImage));
    });
  }
}
