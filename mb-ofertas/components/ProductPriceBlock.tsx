import { formatPriceTwoDecimals } from "@/lib/format";

type Props = {
  price: string;
  previous_price: string | null;
  discount_pct: string | null;
  installments: string | null;
  installment_max_times?: number | string | null;
  installment_unit_price?: string | null;
  /** Lista compacta (uma linha) ou detalhada */
  variant?: "default" | "compact";
};

export function ProductPriceBlock({
  price,
  previous_price,
  discount_pct,
  installments,
  installment_max_times,
  installment_unit_price,
  variant = "default",
}: Props) {
  const prev = Number(previous_price);
  const cash = Number(price);
  const hasFull = previous_price != null && prev > 0 && cash > 0 && prev > cash;
  const maxTimes =
    installment_max_times != null && String(installment_max_times).trim() !== ""
      ? Number(installment_max_times)
      : null;
  const unit =
    installment_unit_price != null && String(installment_unit_price).trim() !== ""
      ? Number(installment_unit_price)
      : null;
  const hasParcel = maxTimes != null && maxTimes > 0 && unit != null && unit > 0 && Number.isFinite(unit);

  if (variant === "compact") {
    return (
      <div className="mt-1.5 flex flex-wrap items-center gap-2 text-sm">
        {hasFull && (
          <>
            <span className="text-stone-400 line-through">R$ {formatPriceTwoDecimals(prev)}</span>
            <span className="font-semibold text-amber-700">à vista R$ {formatPriceTwoDecimals(cash)}</span>
          </>
        )}
        {!hasFull && (
          <span className="font-semibold text-amber-700">R$ {formatPriceTwoDecimals(cash)}</span>
        )}
        {hasParcel && (
          <span className="text-stone-600">
            · até {maxTimes}x R$ {formatPriceTwoDecimals(unit)}
          </span>
        )}
        {!hasParcel && installments?.trim() && (
          <span className="text-stone-500">· {installments}</span>
        )}
        {hasFull && discount_pct && (
          <span className="badge bg-amber-100 text-amber-800">{discount_pct}% OFF</span>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-1.5 text-sm">
      {hasFull && (
        <p>
          <span className="text-stone-500">Preço cheio: </span>
          <span className="text-stone-400 line-through">R$ {formatPriceTwoDecimals(prev)}</span>
        </p>
      )}
      <p>
        <span className="text-stone-600">À vista: </span>
        <span className="text-lg font-semibold text-amber-700">R$ {formatPriceTwoDecimals(cash)}</span>
        {hasFull && discount_pct && (
          <span className="ml-2 badge bg-amber-100 text-amber-800">{discount_pct}% OFF</span>
        )}
        {!hasFull && discount_pct && (
          <span className="ml-2 badge bg-amber-100 text-amber-800">{discount_pct}% OFF</span>
        )}
      </p>
      {hasParcel && (
        <p className="text-stone-800">
          <span className="text-stone-600">Parcelado: </span>
          até <strong>{maxTimes}x</strong> de <strong>R$ {formatPriceTwoDecimals(unit)}</strong>
        </p>
      )}
      {!hasParcel && installments?.trim() && (
        <p className="text-stone-600">
          <span className="text-stone-500">Parcelamento: </span>
          {installments}
        </p>
      )}
    </div>
  );
}
