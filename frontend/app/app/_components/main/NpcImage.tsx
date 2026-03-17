import { sendGetNpcImage } from "@/libs/sendGetNpcImage";
import { useEffect, useState } from "react";

export interface NpcImageProps {
    sessionToken: string;
}

export default function NpcImage({ sessionToken }: NpcImageProps) {
    const [imageSrc, setImageSrc] = useState<string>();

    useEffect(() => {
        const fetchImage = async () => {
            const imageBlob = await sendGetNpcImage(sessionToken)
            const localUrl = URL.createObjectURL(imageBlob);
            setImageSrc(localUrl);
        };

        fetchImage();

        return () => imageSrc ? URL.revokeObjectURL(imageSrc) : undefined;
    }, []);

    return <img className="h-full w-full" src={imageSrc} alt="Fetched Blob" />;
}