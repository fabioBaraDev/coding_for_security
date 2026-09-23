INSERT INTO professores (nome, email, especialidade) VALUES
    ('Carlos Silva', 'carlos.silva@escola.com', 'Seguranca da Informacao'),
    ('Ana Oliveira', 'ana.oliveira@escola.com', 'Banco de Dados'),
    ('Roberto Santos', 'roberto.santos@escola.com', 'Desenvolvimento Web')
ON CONFLICT DO NOTHING;

INSERT INTO cursos (nome, descricao, carga_horaria, professor_id) VALUES
    ('Cybersecurity', 'Fundamentos de seguranca cibernetica', 80, 1),
    ('Banco de Dados', 'Modelagem e administracao de bancos de dados', 60, 2),
    ('Desenvolvimento Web', 'Criacao de aplicacoes web com Python', 100, 3)
ON CONFLICT DO NOTHING;

INSERT INTO alunos (nome, email, data_nascimento, cpf) VALUES
    ('Joao Souza', 'joao.souza@aluno.com', '2000-05-15', '111.222.333-44'),
    ('Maria Lima', 'maria.lima@aluno.com', '2001-08-22', '555.666.777-88'),
    ('Pedro Costa', 'pedro.costa@aluno.com', '1999-12-03', '999.000.111-22')
ON CONFLICT DO NOTHING;

INSERT INTO matriculas (aluno_id, curso_id, data_matricula, status) VALUES
    (1, 1, '2024-02-01', 'ativa'),
    (1, 2, '2024-02-01', 'ativa'),
    (2, 1, '2024-02-01', 'ativa'),
    (3, 3, '2024-02-01', 'ativa')
ON CONFLICT DO NOTHING;

INSERT INTO notas (matricula_id, valor, descricao, data_avaliacao) VALUES
    (1, 8.5, 'Prova 1', '2024-03-15'),
    (1, 9.0, 'Prova 2', '2024-05-10'),
    (2, 7.0, 'Prova 1', '2024-03-15'),
    (3, 6.5, 'Prova 1', '2024-03-15'),
    (4, 9.5, 'Prova 1', '2024-03-15');
