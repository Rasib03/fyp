part of 'image_capture_bloc.dart';

@immutable
sealed class ImageCaptureEvent {}

class ImageCaptureRequest extends ImageCaptureEvent {
  ImageCaptureRequest();
}

class ImageCapturedEvent extends ImageCaptureEvent {
  final XFile? image;

  ImageCapturedEvent({this.image});
}

class ImageGalleryRequest extends ImageCaptureEvent {
  ImageGalleryRequest();
}
