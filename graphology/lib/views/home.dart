import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:graphology/blocs/bloc/image_capture_bloc.dart';
import 'package:graphology/blocs/bloc/internet_checker_bloc.dart';
import 'package:graphology/views/analze_handwriting.dart';
import 'package:graphology/views/camera_screen.dart';
import 'package:graphology/widgets/select_option_widget.dart';

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
              } else if (state is ImageCapturedState) {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) =>
                        AnalyzeHandwriting(image: state.image),
                  ),
                );
              } else if (state is ImageGalleryPicked && state.image != null) {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) =>
                        AnalyzeHandwriting(image: state.image),
                  ),
                );
              }
            },
          ),
        ],
        child: BlocBuilder<ImageCaptureBloc, ImageCaptureState>(
          builder: (context, captureState) {
            return SelectOptionWidget(MediaQuery.sizeOf(context), context);
          },
        ),
      ),
    );
  }
}
