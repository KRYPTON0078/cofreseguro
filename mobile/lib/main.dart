import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/api_client.dart';
import 'services/session.dart';
import 'screens/login_screen.dart';
import 'screens/home_shell.dart';
import 'l10n/app_strings.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final session = SessionState();
  await session.load();
  runApp(CofreSeguroApp(session: session));
}

class CofreSeguroApp extends StatelessWidget {
  const CofreSeguroApp({super.key, required this.session});
  final SessionState session;

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: session),
        Provider(create: (_) => ApiClient()),
      ],
      child: Consumer<SessionState>(
        builder: (context, s, _) {
          final t = AppStrings(s.locale);
          return MaterialApp(
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
            onGenerateTitle: (_) => t.appName,
          );
        },
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
