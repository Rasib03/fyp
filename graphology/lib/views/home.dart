import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:graphology/blocs/bloc/image_capture_bloc.dart';
import 'package:graphology/blocs/bloc/internet_checker_bloc.dart';
import 'package:graphology/views/camera_screen.dart';
import 'package:graphology/widgets/analyze_handwriting.dart';
import 'package:graphology/widgets/select_option.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  void initState() {
    context.read<InternetCheckerBloc>().add(StartListeningConnection());
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Graphology',
          style: TextStyle(fontSize: 27, fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
      ),
      body: MultiBlocListener(
        listeners: [
          BlocListener<InternetCheckerBloc, InternetCheckerState>(
            listener: (context, state) {
              if (state is InternetConnected) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Internet connection restored'),
                    backgroundColor: Colors.green,
                    duration: Duration(seconds: 2),
                  ),
                );
              } else if (state is InternetDisconnected) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('No internet connection'),
                    backgroundColor: Colors.red,
                    duration: Duration(seconds: 2),
                  ),
                );
              }
            },
          ),
          BlocListener<ImageCaptureBloc, ImageCaptureState>(
            listener: (context, state) {
              if (state is OpenCameraScreen) {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => CameraScreen()),
                );
              } else if (state is ImageCapturedState) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Image captured successfully!'),
                    backgroundColor: Colors.green,
                  ),
                );
              }
            },
          ),
        ],
        child: BlocBuilder<ImageCaptureBloc, ImageCaptureState>(
          builder: (context, captureState) {
            if (captureState is ImageCapturedState) {
              return AnalyzeHandwriting(
                MediaQuery.sizeOf(context),
                captureState.image,
                context,
              );
            } else if (captureState is ImageGalleryPicked) {
              return AnalyzeHandwriting(
                MediaQuery.sizeOf(context),
                captureState.image,
                context,
              );
            }
            return SelectOption(MediaQuery.sizeOf(context), context);
          },
        ),
      ),
    );
  }
}
