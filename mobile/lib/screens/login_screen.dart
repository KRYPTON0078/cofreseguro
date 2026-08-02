import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_strings.dart';
import '../services/api_client.dart';
import '../services/session.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final email = TextEditingController(text: 'demo@cofreseguro.app');
  final password = TextEditingController(text: 'demo123!');
  bool loading = false;
  String? error;

  Future<void> _login() async {
    final session = context.read<SessionState>();
    final t = AppStrings(session.locale);
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final token = await context.read<ApiClient>().login(
            session.apiBase,
            email.text.trim(),
            password.text,
          );
      await session.setToken(token);
    } catch (_) {
      setState(() => error = t.loginFailed);
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final session = context.watch<SessionState>();
    final t = AppStrings(session.locale);
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF0B3D34), Color(0xFF1B6B5A), Color(0xFF0F5C4C)],
          ),
        ),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Card(
              margin: const EdgeInsets.all(24),
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text(t.appName, style: Theme.of(context).textTheme.headlineMedium),
                    const SizedBox(height: 4),
                    Text(t.tagline),
                    const SizedBox(height: 16),
                    TextField(
                      controller: email,
                      decoration: InputDecoration(labelText: t.email),
                    ),
                    TextField(
                      controller: password,
                      obscureText: true,
                      decoration: InputDecoration(labelText: t.password),
                    ),
                    const SizedBox(height: 8),
                    Text(t.demoHint, style: Theme.of(context).textTheme.bodySmall),
                    if (error != null)
                      Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: Text(error!, style: const TextStyle(color: Colors.red)),
                      ),
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: loading ? null : _login,
                      child: Text(loading ? '...' : t.signIn),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
