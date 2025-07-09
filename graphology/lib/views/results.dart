import 'package:flutter/material.dart';
import 'package:graphology/models/response.dart';

class Results extends StatelessWidget {
  final Response? analysisResult;
  const Results({super.key, required this.analysisResult});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            Text(
              'Emotional Stability: ${analysisResult?.trait1 ?? 'N/A'}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            Text(
              'Mental Energy: ${analysisResult?.trait2 ?? 'N/A'}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            Text(
              'Modesty: ${analysisResult?.trait3 ?? 'N/A'}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            Text(
              'Personal Harmony and Flexibility: ${analysisResult?.trait4 ?? 'N/A'}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            Text(
              'Lack of Discipline: ${analysisResult?.trait5 ?? 'N/A'}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            Text(
              'Poor Concentration: ${analysisResult?.trait6 ?? 'N/A'}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            Text(
              'Non Communicativeness: ${analysisResult?.trait7 ?? 'N/A'}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            Text(
              'Social Isolation: ${analysisResult?.trait8 ?? 'N/A'}',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }
}
