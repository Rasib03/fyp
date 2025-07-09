import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:graphology/blocs/bloc/analyze_handwriting_bloc.dart';
import 'package:graphology/blocs/bloc/image_capture_bloc.dart';
import 'package:graphology/blocs/bloc/internet_checker_bloc.dart';
import 'package:graphology/views/home.dart';
import 'package:internet_connection_checker/internet_connection_checker.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider<InternetCheckerBloc>(
          create: (context) => InternetCheckerBloc(
            connectionChecker: InternetConnectionChecker.instance,
          ),
        ),

        BlocProvider<ImageCaptureBloc>(create: (context) => ImageCaptureBloc()),
        BlocProvider<AnalyzeHandwritingBloc>(
          create: (context) => AnalyzeHandwritingBloc(),
        ),
      ],

      child: MaterialApp(
        title: 'CameraAwesome Example',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        ),
        home: const Home(),
      ),
    );
  }
}
