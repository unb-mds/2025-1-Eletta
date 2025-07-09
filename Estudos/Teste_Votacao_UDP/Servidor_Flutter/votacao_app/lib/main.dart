import 'package:flutter/material.dart';
import 'package:udp/udp.dart';
import 'dart:io'; // Para InternetAddress

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Votação',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const VotacaoPage(),
    );
  }
}

class VotacaoPage extends StatefulWidget {
  const VotacaoPage({Key? key}) : super(key: key);

  @override
  _VotacaoPageState createState() => _VotacaoPageState();
}

class _VotacaoPageState extends State<VotacaoPage> {
  // Controlador do campo de texto para a pergunta
  final TextEditingController _perguntaController = TextEditingController();

  Future<void> enviarVoto(String voto) async {
    var sender = await UDP.bind(Endpoint.any());

    await sender.send(
      voto.codeUnits,
      Endpoint.unicast(
        InternetAddress('xxxx'), // <-- Aqui você coloca o IP do servidor! ##############################################################
        port: Port(5000),
      ),
    );

    sender.close();
  }

  void _votar(BuildContext context, String voto) {
    enviarVoto(voto);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Voto "$voto" enviado!')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Votação')),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Campo de texto para digitar a pergunta
            TextField(
              controller: _perguntaController,
              decoration: InputDecoration(
                labelText: 'Digite a pergunta da votação',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),

            // Exibe a pergunta digitada
            if (_perguntaController.text.isNotEmpty)
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  'Pergunta: ${_perguntaController.text}',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
              ),

            const SizedBox(height: 30),

            // Botões de votação
            ElevatedButton(
              onPressed: () => _votar(context, 'a favor'),
              child: const Text('A Favor'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _votar(context, 'contra'),
              child: const Text('Contra'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _votar(context, 'abster'),
              child: const Text('Abster'),
            ),
          ],
        ),
      ),
    );
  }
}
