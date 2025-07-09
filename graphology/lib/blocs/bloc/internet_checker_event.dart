part of 'internet_checker_bloc.dart';

@immutable
sealed class InternetCheckerEvent {}

class StartListeningConnection extends InternetCheckerEvent {}

class StopListeningConnection extends InternetCheckerEvent {}

class ConnectionStatusChanged extends InternetCheckerEvent {
  final InternetConnectionStatus status;

  ConnectionStatusChanged(this.status);
}
