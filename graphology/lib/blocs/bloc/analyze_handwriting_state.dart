part of 'analyze_handwriting_bloc.dart';

@immutable
sealed class AnalyzeHandwritingState {}

final class AnalyzeHandwritingInitial extends AnalyzeHandwritingState {}

class HandwritingAnalyzed extends AnalyzeHandwritingState {
  final Response analysisResult;

  HandwritingAnalyzed({required this.analysisResult});
}
