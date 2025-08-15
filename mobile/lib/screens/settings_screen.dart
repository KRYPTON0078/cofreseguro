import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/session.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final session = context.watch<SessionState>();
    return ListView(children: [
      ListTile(
        title: const Text('Language / Idioma'),
        trailing: DropdownButton<String>(
          value: session.locale,
          items: const [
            DropdownMenuItem(value: 'en', child: Text('English')),
            DropdownMenuItem(value: 'pt', child: Text('Português')),
          ],
          onChanged: (v) { if (v != null) context.read<SessionState>().setLocale(v); },
        ),
      ),
      ListTile(title: const Text('Sign out'), onTap: () => context.read<SessionState>().clear()),
    ]);
  }
}
