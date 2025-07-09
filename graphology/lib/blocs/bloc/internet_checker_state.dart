part of 'internet_checker_bloc.dart';

@immutable
sealed class InternetCheckerState {}

class InternetCheckerInitial extends InternetCheckerState {}

class InternetConnected extends InternetCheckerState {}

class InternetDisconnected extends InternetCheckerState {}
