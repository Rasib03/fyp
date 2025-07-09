import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:graphology/blocs/bloc/analyze_handwriting_bloc.dart';
import 'package:graphology/views/results.dart';
import 'package:graphology/widgets/analyze_handwriting_widget.dart';
import 'package:image_picker/image_picker.dart';

class AnalyzeHandwriting extends StatelessWidget {
  final XFile? image;
  const AnalyzeHandwriting({super.key, required this.image});

  @override
  Widget build(BuildContext context) {
    final mq = MediaQuery.of(context).size;
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Analyze Handwriting',
          style: TextStyle(fontSize: 27, fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
      ),
      body: BlocListener<AnalyzeHandwritingBloc, AnalyzeHandwritingState>(
        listener: (context, state) {
          if (state is HandwritingAnalyzed) {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) =>
                    Results(analysisResult: state.analysisResult),
              ),
            );
          } else if (state is AnalyzeHandwritingInitial) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Error analyzing handwriting. Please try again.'),
                backgroundColor: Colors.red,
                duration: Duration(seconds: 2),
              ),
            );
          }
        },
        child: AnalyzeHandwritingWidget(mq, image, context),
      ),
    );
  }
}
