-- MB-OFERTAS - Schema PostgreSQL (Supabase)
-- Executado por migrate.ts

-- Categorias (eletrônicos, livros, católicos, etc.)
CREATE TABLE IF NOT EXISTS categories (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name       VARCHAR(100) NOT NULL UNIQUE,
  slug       VARCHAR(100) NOT NULL UNIQUE,
  is_active  BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Produtos (ofertas de afiliados)
CREATE TABLE IF NOT EXISTS products (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category_id     UUID REFERENCES categories(id) ON DELETE SET NULL,
  external_id     VARCHAR(255),           -- ID na Amazon/outro
  title           VARCHAR(500) NOT NULL,
  price           DECIMAL(12,2) NOT NULL,
  previous_price  DECIMAL(12,2),
  discount_pct    DECIMAL(5,2),
  affiliate_link  TEXT NOT NULL,
  image_url       TEXT,
  source          VARCHAR(50) NOT NULL DEFAULT 'amazon',  -- amazon, manual, etc.
  status          VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, approved, rejected, sent
  approved_at     TIMESTAMPTZ,
  approved_by     UUID,
  installments    TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(external_id, source)
);

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_created ON products(created_at DESC);

-- Campanhas (agrupam envios)
CREATE TABLE IF NOT EXISTS campaigns (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name         VARCHAR(200) NOT NULL,
  status       VARCHAR(20) NOT NULL DEFAULT 'draft',  -- draft, scheduled, sending, completed, cancelled
  scheduled_at TIMESTAMPTZ,
  started_at   TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  product_ids  UUID[] DEFAULT '{}',
  target_type  VARCHAR(20) NOT NULL DEFAULT 'list',  -- list, group, broadcast
  target_ref   TEXT,                                 -- lista id, grupo id, etc.
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_scheduled ON campaigns(scheduled_at);

-- Mensagens geradas (copy + link de rastreamento)
CREATE TABLE IF NOT EXISTS messages (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id   UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  product_id     UUID REFERENCES products(id) ON DELETE CASCADE,
  body          TEXT NOT NULL,
  short_link    TEXT,
  status        VARCHAR(20) NOT NULL DEFAULT 'pending', -- pending, sent, failed
  sent_at       TIMESTAMPTZ,
  recipient     VARCHAR(50),  -- phone ou grupo
  error_message TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_messages_campaign ON messages(campaign_id);
CREATE INDEX IF NOT EXISTS idx_messages_product ON messages(product_id);
CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status);

-- Usuários (opcional - para login no dashboard)
CREATE TABLE IF NOT EXISTS users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      VARCHAR(255) NOT NULL UNIQUE,
  name       VARCHAR(200),
  role       VARCHAR(20) NOT NULL DEFAULT 'admin',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Controle de envio (anti-spam)
CREATE TABLE IF NOT EXISTS send_counters (
  id         SERIAL PRIMARY KEY,
  window_at  TIMESTAMPTZ NOT NULL,  -- início da janela (ex: minuto)
  count      INT NOT NULL DEFAULT 0,
  UNIQUE(window_at)
);

-- Seed categorias dos canais
INSERT INTO categories (name, slug) VALUES
  ('Health', 'health'),
  ('Tech', 'tech'),
  ('Ofertas', 'ofertas'),
  ('Faith', 'faith'),
  ('Fitness', 'fitness')
ON CONFLICT (slug) DO NOTHING;

-- Coluna installments (para bancos já existentes)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'products' AND column_name = 'installments') THEN
    ALTER TABLE products ADD COLUMN installments TEXT;
  END IF;
END $$;

-- Parcelamento estruturado (complementa o texto em installments)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'products' AND column_name = 'installment_max_times') THEN
    ALTER TABLE products ADD COLUMN installment_max_times INT;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'products' AND column_name = 'installment_unit_price') THEN
    ALTER TABLE products ADD COLUMN installment_unit_price DECIMAL(12,2);
  END IF;
END $$;

-- Canais WhatsApp: phone = número (wa.me) ou channel_link = link do canal público (ex.: mb.OFERTAS)
CREATE TABLE IF NOT EXISTS whatsapp_channels (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          VARCHAR(200) NOT NULL,
  phone         VARCHAR(20) NOT NULL DEFAULT '',
  channel_link  TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_channels_phone ON whatsapp_channels(phone);
-- Permitir canal só com channel_link (phone vazio)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'whatsapp_channels' AND column_name = 'channel_link') THEN
    ALTER TABLE whatsapp_channels ADD COLUMN channel_link TEXT;
  END IF;
END $$;

-- Qual categoria/canal de ofertas este registro representa (health, tech, ofertas, faith, fitness) — alinha com GitHub Actions CHANNEL_SLUG
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'whatsapp_channels' AND column_name = 'category_slug') THEN
    ALTER TABLE whatsapp_channels ADD COLUMN category_slug VARCHAR(100);
  END IF;
END $$;

-- Links curtos (redirect): código único -> URL longa (opensource, self-hosted)
CREATE TABLE IF NOT EXISTS short_links (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code       VARCHAR(16) NOT NULL UNIQUE,
  long_url   TEXT NOT NULL,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  click_count INT NOT NULL DEFAULT 0,
  last_clicked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_short_links_code ON short_links(code);
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'short_links' AND column_name = 'click_count') THEN
    ALTER TABLE short_links ADD COLUMN click_count INT NOT NULL DEFAULT 0;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'short_links' AND column_name = 'last_clicked_at') THEN
    ALTER TABLE short_links ADD COLUMN last_clicked_at TIMESTAMPTZ;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'short_links' AND column_name = 'product_id') THEN
    ALTER TABLE short_links ADD COLUMN product_id UUID REFERENCES products(id) ON DELETE SET NULL;
  END IF;
END $$;
CREATE INDEX IF NOT EXISTS idx_short_links_product_id ON short_links(product_id);

-- Agendamentos WhatsApp (postagem programada para um canal)
CREATE TABLE IF NOT EXISTS whatsapp_scheduled (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  channel_id   UUID NOT NULL REFERENCES whatsapp_channels(id) ON DELETE CASCADE,
  message      TEXT NOT NULL,
  scheduled_at  TIMESTAMPTZ NOT NULL,
  status       VARCHAR(20) NOT NULL DEFAULT 'pending',
  opened_at    TIMESTAMPTZ,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_whatsapp_scheduled_at ON whatsapp_scheduled(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_whatsapp_scheduled_status ON whatsapp_scheduled(status);
