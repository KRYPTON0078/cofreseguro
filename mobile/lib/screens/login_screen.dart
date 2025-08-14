import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
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
    setState(() { loading = true; error = null; });
    try {
      final token = await context.read<ApiClient>().login(email.text.trim(), password.text);
      context.read<SessionState>().setToken(token);
    } catch (_) {
      setState(() { error = 'Login failed'; });
    } finally {
      setState(() { loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(colors: [Color(0xFF0B3D34), Color(0xFF1B6B5A)]),
        ),
        child: Center(
          child: Card(
            margin: const EdgeInsets.all(24),
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                Text('CofreSeguro', style: Theme.of(context).textTheme.headlineMedium),
                const Text('Mobile-money fraud shield'),
                TextField(controller: email, decoration: const InputDecoration(labelText: 'Email')),
                TextField(controller: password, obscureText: true, decoration: const InputDecoration(labelText: 'Password')),
                if (error != null) Text(error!, style: const TextStyle(color: Colors.red)),
                FilledButton(onPressed: loading ? null : _login, child: Text(loading ? '...' : 'Sign in')),
              ]),
            ),
          ),
        ),
      ),
    );
  }
}
