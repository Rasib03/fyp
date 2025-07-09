part of 'image_capture_bloc.dart';

@immutable
sealed class ImageCaptureState {}

final class ImageCaptureInitial extends ImageCaptureState {}

class ImageCapturedState extends ImageCaptureState {
  final XFile? image;

  ImageCapturedState({this.image});
}

class OpenCameraScreen extends ImageCaptureState {
  OpenCameraScreen();
}

class ImageGalleryPicked extends ImageCaptureState {
  final XFile? image;
  ImageGalleryPicked({required this.image});
}
