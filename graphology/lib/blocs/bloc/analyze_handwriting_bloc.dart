import 'package:bloc/bloc.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:graphology/models/response.dart';
import 'package:http/http.dart' as http;
import 'package:meta/meta.dart';
import 'dart:convert';

part 'analyze_handwriting_event.dart';
part 'analyze_handwriting_state.dart';

class AnalyzeHandwritingBloc
    extends Bloc<AnalyzeHandwritingEvent, AnalyzeHandwritingState> {
  AnalyzeHandwritingBloc() : super(AnalyzeHandwritingInitial()) {
    on<AnalyzeHandwritingImageSelected>((event, emit) async {
      try {
        final response = await analyzeHandwriting(event.imagePath);
        emit(HandwritingAnalyzed(analysisResult: response));
      } catch (e) {
        emit(AnalyzeHandwritingInitial());
      }
    });
  }

  Future<Response> analyzeHandwriting(String imagePath) async {
    final url = Uri.parse('https://fyp-qeyn.onrender.com/analyze');
    final request = http.MultipartRequest('POST', url);

    // Add the API key header
    request.headers['x_api_key'] = dotenv.env['API_KEY'] ?? '';

    // Attach the image file
    request.files.add(await http.MultipartFile.fromPath('file', imagePath));

    // Send the request
    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return Response(
        trait1: data['trait_1'] ?? '',
        trait2: data['trait_2'] ?? '',
        trait3: data['trait_3'] ?? '',
        trait4: data['trait_4'] ?? '',
        trait5: data['trait_5'] ?? '',
        trait6: data['trait_6'] ?? '',
        trait7: data['trait_7'] ?? '',
        trait8: data['trait_8'] ?? '',
      );
    } else if (response.statusCode == 401) {
      throw Exception('Invalid API Key');
    } else if (response.statusCode == 400) {
      throw Exception('Invalid image format');
    } else {
      throw Exception(
        'Failed to analyze handwriting. Code: ${response.statusCode}',
      );
    }
  }
}
