part of 'analyze_handwriting_bloc.dart';

@immutable
sealed class AnalyzeHandwritingEvent {}

class AnalyzeHandwritingImageSelected extends AnalyzeHandwritingEvent {
  final String imagePath;

  AnalyzeHandwritingImageSelected(this.imagePath);
}
