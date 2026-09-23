CREATE TABLE IF NOT EXISTS professores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    especialidade VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS cursos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    carga_horaria INTEGER NOT NULL,
    professor_id INTEGER REFERENCES professores(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_nascimento DATE,
    cpf VARCHAR(14) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS matriculas (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES alunos(id) ON DELETE CASCADE,
    curso_id INTEGER NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,
    data_matricula DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'ativa',
    UNIQUE(aluno_id, curso_id)
);

CREATE TABLE IF NOT EXISTS notas (
    id SERIAL PRIMARY KEY,
    matricula_id INTEGER NOT NULL REFERENCES matriculas(id) ON DELETE CASCADE,
    valor NUMERIC(4,2) NOT NULL CHECK (valor >= 0 AND valor <= 10),
    descricao VARCHAR(100),
    data_avaliacao DATE NOT NULL DEFAULT CURRENT_DATE
);
