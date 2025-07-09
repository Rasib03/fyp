import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:graphology/blocs/bloc/image_capture_bloc.dart';

Widget SelectOptionWidget(Size mq, BuildContext context) {
  return Center(
    child: Column(
      children: [
        Text(
          'Please select an option',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.w600),
        ),
        SizedBox(height: mq.height * .3),
        GestureDetector(
          onTap: () {
            context.read<ImageCaptureBloc>().add(ImageGalleryRequest());
          },
          child: Container(
            width: mq.width * .9,
            height: mq.height * .1,
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border.all(color: Colors.blue, width: 1.5),
              borderRadius: BorderRadius.circular(50),
            ),
            child: Center(
              child: Text(
                'Galary',
                style: TextStyle(
                  color: Colors.blue,
                  fontSize: 25,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ),
        SizedBox(height: mq.height * .05),
        GestureDetector(
          onTap: () {
            context.read<ImageCaptureBloc>().add(ImageCaptureRequest());
          },
          child: Container(
            width: mq.width * .9,
            height: mq.height * .1,
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border.all(color: Colors.blue, width: 1.5),
              borderRadius: BorderRadius.circular(50),
            ),
            child: Center(
              child: Text(
                'Camera',
                style: TextStyle(
                  color: Colors.blue,
                  fontSize: 25,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ),
      ],
    ),
  );
}
