Create a database on supabase 

Open the Supabase SQLEditor and run :

CREATE TABLE IF NOT EXISTS dinosaurs (
  id               SERIAL PRIMARY KEY,
  name             TEXT           NOT NULL,
  period           TEXT           NOT NULL,
  diet             TEXT           NOT NULL,
  length_m         NUMERIC(5,1)   CHECK (length_m > 0),
  weight_kg        INTEGER        CHECK (weight_kg > 0),
  discovered_year  INTEGER        CHECK (discovered_year BETWEEN 1800 AND 2100),
  found_in         TEXT,
  fun_fact         TEXT,
  created_at       TIMESTAMPTZ    NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_dinos_period ON dinosaurs (period);
CREATE INDEX IF NOT EXISTS idx_dinos_diet   ON dinosaurs (diet);


INSERT INTO dinosaurs
  (name, period, diet, length_m, weight_kg, discovered_year, found_in, fun_fact)
VALUES
  ('Tyrannosaurus rex',    'Late Cretaceous',  'Carnivore',   12.3,  8000, 1902, 'Montana, USA',       'Could bite with 57,000 N of force — the most of any land animal'),
  ('Triceratops',           'Late Cretaceous',  'Herbivore',    9.0,  12000, 1887, 'Wyoming, USA',       'Its three horns could each grow over 1 metre long'),
  ('Velociraptor',          'Late Cretaceous',  'Carnivore',    2.0,    15, 1924, 'Mongolia',           'Was actually feathered and about the size of a turkey'),
  ('Brachiosaurus',         'Late Jurassic',    'Herbivore',   26.0,  56000, 1900, 'Colorado, USA',      'Its nostrils were on top of its head, not its snout'),
  ('Stegosaurus',           'Late Jurassic',    'Herbivore',    9.0,   5000, 1877, 'Colorado, USA',      'Its brain was about the size of a walnut'),
  ('Spinosaurus',           'Early Cretaceous', 'Carnivore',   15.0,  20000, 1912, 'Egypt',               'Likely spent most of its life in water, like a giant crocodile'),
  ('Ankylosaurus',          'Late Cretaceous',  'Herbivore',    6.5,   6000, 1908, 'Montana, USA',       'Its tail club could shatter bone and was swung at up to 30 km/h'),
  ('Pteranodon',            'Late Cretaceous',  'Piscivore',    1.8,    20, 1876, 'Kansas, USA',        'Not a dinosaur — a pterosaur, with a wingspan up to 7 metres'),
  ('Diplodocus',            'Late Jurassic',    'Herbivore',   27.0,  16000, 1877, 'Wyoming, USA',       'Could crack its tail like a whip, producing a sonic boom'),
  ('Pachycephalosaurus',    'Late Cretaceous',  'Omnivore',     4.5,   450, 1931, 'South Dakota, USA',  'Its domed skull was 25 cm thick — used for head-butting rivals');

  To deploy Install: pip install -r requirements.tx
  
  Command: uvicorn main:app --host 0.0.0.0 --port $PORT

  Enviroment Variables: SUPABASE_URL SUPABASE_KEY SECRET_KEY
