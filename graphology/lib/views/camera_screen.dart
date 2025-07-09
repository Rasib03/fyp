import 'package:camerawesome/camerawesome_plugin.dart';
import 'package:camerawesome/pigeon.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:graphology/blocs/bloc/image_capture_bloc.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CameraAwesomeBuilder.awesome(
        onMediaCaptureEvent: (event) async {
          switch ((event.status, event.isPicture)) {
            case (MediaCaptureStatus.capturing, true):
              debugPrint('Capturing picture...');
              break;

            case (MediaCaptureStatus.success, true):
              await event.captureRequest.when(
                single: (p0) async {
                  debugPrint('Picture saved at: ${p0.path}');
                  context.read<ImageCaptureBloc>().add(
                    ImageCapturedEvent(image: XFile(p0.path!)),
                  );

                  // Return the XFile
                  Navigator.of(context).pop();
                },
              );
              break;
            case (MediaCaptureStatus.failure, true):
              debugPrint('Failed to capture picture: ${event.exception}');
              Navigator.of(context).pop(null);
              break;

            default:
              debugPrint('Unhandled capture event');
          }
        },
        saveConfig: SaveConfig.photo(
          pathBuilder: (sensors) async {
            final extDir = Directory('/storage/emulated/0/DCIM/Camera');
            await extDir.create(recursive: true);

            final String filePath =
                '${extDir.path}/${DateTime.now().millisecondsSinceEpoch}.jpg';
            return SingleCaptureRequest(filePath, sensors.first);
          },
          exifPreferences: ExifPreferences(saveGPSLocation: true),
        ),
        sensorConfig: SensorConfig.single(
          sensor: Sensor.position(SensorPosition.back),
          flashMode: FlashMode.auto,
          aspectRatio: CameraAspectRatios.ratio_4_3,
          zoom: 0.0,
        ),
        enablePhysicalButton: true,
        previewAlignment: Alignment.center,
        previewFit: CameraPreviewFit.contain,
        availableFilters: awesomePresetFiltersList,
      ),
    );
  }
}
