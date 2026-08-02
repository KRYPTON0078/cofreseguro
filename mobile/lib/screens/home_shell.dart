import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_strings.dart';
import '../services/session.dart';
import 'analyze_screen.dart';
import 'history_screen.dart';
import 'tips_screen.dart';
import 'settings_screen.dart';

class HomeShell extends StatefulWidget {
  const HomeShell({super.key});
  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int index = 0;

  @override
  Widget build(BuildContext context) {
    final t = AppStrings(context.watch<SessionState>().locale);
    const pages = [AnalyzeScreen(), HistoryScreen(), TipsScreen(), SettingsScreen()];
    return Scaffold(
      appBar: AppBar(title: Text(t.appName)),
      body: pages[index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (i) => setState(() => index = i),
        destinations: [
          NavigationDestination(icon: const Icon(Icons.shield_outlined), label: t.analyze),
          NavigationDestination(icon: const Icon(Icons.history), label: t.history),
          NavigationDestination(icon: const Icon(Icons.lightbulb_outline), label: t.tips),
          NavigationDestination(icon: const Icon(Icons.settings), label: t.settings),
        ],
      ),
    );
  }
}
