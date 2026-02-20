"use client";

import { logAffiliateClick } from "@/data/affiliates";
import { Button } from "@/components/ui/button";
import { ExternalLink } from "lucide-react";

interface AmazonButtonProps {
  url: string;
  productId: string;
  productTitle: string;
}

export function AmazonButton({ url, productId, productTitle }: AmazonButtonProps) {
  return (
    <Button variant="outline" size="lg" asChild>
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        onClick={() => logAffiliateClick(productId, productTitle)}
      >
        Ver na Amazon
        <ExternalLink className="ml-2 h-4 w-4" />
      </a>
    </Button>
  );
}
