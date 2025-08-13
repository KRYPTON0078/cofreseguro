import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/api_client.dart';
import 'services/session.dart';
import 'screens/login_screen.dart';
import 'screens/home_shell.dart';

void main() {
  runApp(const CofreSeguroApp());
}

class CofreSeguroApp extends StatelessWidget {
  const CofreSeguroApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SessionState()),
        Provider(create: (_) => ApiClient(baseUrl: 'http://localhost:8080')),
      ],
      child: MaterialApp(
        title: 'CofreSeguro',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF0F5C4C),
            brightness: Brightness.light,
          ),
          useMaterial3: true,
        ),
        home: const RootGate(),
      ),
    );
  }
}

class RootGate extends StatelessWidget {
  const RootGate({super.key});

  @override
  Widget build(BuildContext context) {
    final session = context.watch<SessionState>();
    if (session.token == null) return const LoginScreen();
    return const HomeShell();
  }
}
