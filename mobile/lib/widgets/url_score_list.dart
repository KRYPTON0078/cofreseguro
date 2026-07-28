import 'package:flutter/material.dart';

class UrlScoreList extends StatelessWidget {
  const UrlScoreList({super.key, required this.items});
  final List<Map<String, dynamic>> items;

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) return const SizedBox.shrink();
    return Column(
      children: items
          .map((u) => ListTile(
                leading: const Icon(Icons.link),
                title: Text('${u['url']}'),
                subtitle: Text('score=${u['score']} reasons=${u['reasons']}'),
              ))
          .toList(),
    );
  }
}
