import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:graphology/blocs/bloc/analyze_handwriting_bloc.dart';
import 'package:graphology/blocs/bloc/internet_checker_bloc.dart';
import 'package:image_picker/image_picker.dart';

Widget AnalyzeHandwritingWidget(Size mq, XFile? image, BuildContext context) {
  bool _isConnected = false;
  return BlocListener<InternetCheckerBloc, InternetCheckerState>(
    listener: (context, state) {
      if (state is InternetDisconnected) {
        _isConnected = false;
      } else if (state is InternetConnected) {
        _isConnected = true;
      }
    },
    child: Center(
      child: Column(
        children: [
          SizedBox(height: mq.height * .05),
          Container(
            width: mq.width * .9,
            height: mq.height * .3,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(25),
            ),
            child: image != null
                ? ClipRRect(
                    borderRadius: BorderRadiusGeometry.circular(25),
                    child: Image.file(File(image.path), fit: BoxFit.cover),
                  )
                : Center(
                    child: Text(
                      'No image selected',
                      style: TextStyle(color: Colors.white, fontSize: 20),
                    ),
                  ),
          ),
          SizedBox(height: mq.height * .05),
          GestureDetector(
            onTap: () {
              if (!_isConnected) {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    title: Text(
                      'No Internet Connection',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 20,
                      ),
                    ),
                    content: Text(
                      'Please check your internet connection and try again.',
                      style: TextStyle(fontSize: 16),
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.of(context).pop(),
                        child: Text(
                          'OK',
                          style: TextStyle(color: Colors.deepPurple),
                        ),
                      ),
                    ],
                  ),
                );
              } else {
                context.read<AnalyzeHandwritingBloc>().add(
                  AnalyzeHandwritingImageSelected(image!.path),
                );
              }
            },
            child: Material(
              elevation: 5,
              borderRadius: BorderRadius.circular(25),
              child: Container(
                width: mq.width * .9,
                height: mq.height * .1,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(25),
                  border: Border.all(color: Colors.blue, width: 1.5),
                ),
                child: Center(
                  child: Text(
                    'Analyze Handwriting',
                    style: TextStyle(
                      color: Colors.blue,
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    ),
  );
}
