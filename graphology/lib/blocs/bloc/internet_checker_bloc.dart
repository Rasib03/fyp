import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:meta/meta.dart';
import 'package:internet_connection_checker/internet_connection_checker.dart';

part 'internet_checker_event.dart';
part 'internet_checker_state.dart';

class InternetCheckerBloc
    extends Bloc<InternetCheckerEvent, InternetCheckerState> {
  final InternetConnectionChecker connectionChecker;
  StreamSubscription<InternetConnectionStatus>? _subscription;

  InternetCheckerBloc({required this.connectionChecker})
    : super(InternetCheckerInitial()) {
    on<StartListeningConnection>(_onStartListening);
    on<StopListeningConnection>(_onStopListening);
    on<ConnectionStatusChanged>(_onConnectionStatusChanged);
  }

  void _onStartListening(
    StartListeningConnection event,
    Emitter<InternetCheckerState> emit,
  ) {
    _subscription = connectionChecker.onStatusChange.listen((status) {
      add(ConnectionStatusChanged(status));
    });
  }

  void _onConnectionStatusChanged(
    ConnectionStatusChanged event,
    Emitter<InternetCheckerState> emit,
  ) {
    if (event.status == InternetConnectionStatus.connected) {
      emit(InternetConnected());
    } else {
      emit(InternetDisconnected());
    }
  }

  void _onStopListening(
    StopListeningConnection event,
    Emitter<InternetCheckerState> emit,
  ) {
    _subscription?.cancel();
  }

  @override
  Future<void> close() {
    _subscription?.cancel();
    return super.close();
  }
}
